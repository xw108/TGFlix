from .deps import APIRouter,HTTPException,RedirectResponse,Request,CONFIG,crud,templates


router = APIRouter()



@router.get("/{slug}/p{part}")
async def get_movie(request: Request, slug:str, part:int):
    m = await crud.get_movie_by_slug( slug)
    if not m or m['is_series']:
        raise HTTPException(404, "Page not found")

    if part < 1:
        return RedirectResponse("/movie/" + slug)
    # pr

    epf = await crud.get_movie_episode_files( m['id'], part,1)

    download = CONFIG.DOWNLOAD_ENABLED
    title = m["title"]
    if part > 1:
        title += ' Part'+part
    return templates.TemplateResponse("movie_parts.html", {
        "request": request,
        'mov'   : m,
        'title' : title ,
        'res'   : epf,
        'dwld'  : download
    })

@router.get("/{slug}")
async def get_movie(request: Request, slug:str):
    m = await crud.get_movie_by_slug( slug)
    if not m or m['is_series']:
        raise HTTPException(404, "Page not found")

    # pr
    c = await crud.get_genre_matches( m['genre'])
    s = await crud.get_movie_parts( m['id'])

    
    return templates.TemplateResponse("movie.html", {
        "request": request,
        'movie' : m,
        'seasons' : s,
        'genre' : c
    })

@router.get("")
async def get_movies(request: Request, page:int = 1):
    if page < 1:
        page = 1
    m = await crud.get_movies( (page-1)*CONFIG.MAX_ITEMS_PER_PAGE, CONFIG.MAX_ITEMS_PER_PAGE)
    return templates.TemplateResponse("movies.html",
        {"request": request,'title' : 'Movies','movies' : m,'page':page})

