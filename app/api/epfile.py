from .deps import APIRouter,HTTPException,Request,StreamingResponse,DwnloadManger,\
    CONFIG,crud,tgUtils,client,Response,types


router = APIRouter()



@router.get("/img/{id}.jpg")
async def get_image( id: int, isThump: bool = False):
    i = await crud.get_pic(id=id)
    if not i:
        raise HTTPException(404, "Page not found")

    try:
        ch = tgUtils.get_peer_id( types.PeerChannel(i["ch_id"]))
        m = await client.get_messages(entity= ch, ids=i["msg_id"])
    except:
        raise HTTPException(403, "Acces forbidden. (File not accessable)")

    if not m:
        raise HTTPException(410, "No longer access available")

    thumb = client._get_thumb(
        m.photo.sizes,
        int(len(m.photo.sizes) // 2) if isThump else len(m.photo.sizes) - 1,
    )
    if not thumb or isinstance(thumb, types.PhotoSizeEmpty):
        return HTTPException(410, "No longer access available")

    if isinstance(thumb, (types.PhotoCachedSize, types.PhotoStrippedSize)):
        body = client._download_cached_photo_size(thumb, bytes)
        return Response(
            status_code=200,
            content=body,
            headers={
                "Content-Type": "image/jpeg",
                "Content-Disposition": 'inline; filename="image.jpg"',
            },
        )
    else:
        return StreamingResponse(
            client.iter_download(
                types.InputPhotoFileLocation(
                    id=m.photo.id,
                    access_hash=m.photo.access_hash,
                    file_reference=m.photo.file_reference,
                    thumb_size=thumb.type,
                )
            ),
            headers={
                "Content-Type": "image/jpeg",
                "Content-Disposition": 'inline; filename="image.jpg"',
            },
            media_type="image/jpeg",
        )


@router.get("/thump/{id}.jpg")
async def get_thumpnil_image(id: int):
    return await get_image(id, True)

@router.get("/d/{slug}")
async def get_movie(request: Request, slug:str):
    if not CONFIG.DOWNLOAD_ENABLED:
        raise HTTPException(403, "Acces forbidden. (Download is disabled)")

    if DwnloadManger.downloads >= CONFIG.MAX_SIMULTANIOUS_DOWNLOAD:
        raise HTTPException(403, "Acces forbidden. (Server busy)")

    epf = await crud.get_epfile_by_slug( slug)
    if not epf:
        raise HTTPException(404, "Page not found")

    try:
        ch = tgUtils.get_peer_id( types.PeerChannel( epf["ch_id"]))
        m = await client.get_messages(entity= ch, ids= epf["msg_id"])
    except:
        raise HTTPException(403, "Acces forbidden. (File not accessable)")

    mime_type   = m.file.mime_type
    size        = m.file.size
    ext         = m.file.ext or '.unknown'
    file_name   = epf['slug']+ext
    headers = {
        "Content-Type": mime_type,
        "Content-Length": str(size),
        "Accept-Ranges": "bytes",
        "Content-Disposition": f'attachment; filename="{file_name}"'
    }

    async def decrement_downloads(c):
        DwnloadManger.downloads -= 1
    
    from starlette.background import BackgroundTasks
    tasks = BackgroundTasks()
    tasks.add_task( decrement_downloads, c=epf["ch_id"])
    
    DwnloadManger.downloads += 1
    return StreamingResponse(
        client.iter_download(m.media),
        headers     = headers,
        media_type  = mime_type,
        background  = tasks
    )