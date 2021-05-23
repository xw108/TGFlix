from .deps import APIRouter,HTTPException,RedirectResponse,Request,CONFIG,crud,templates

router = APIRouter()


@router.get("/{slug}/s{season}/e{eps}")
async def get_series_episodes(request: Request, slug:str, season:int, eps:int):
    m = await crud.get_series_by_slug( slug)
    if not m or not m['is_series']:
        raise HTTPException(404, "Page not found")

    if season < 1 or eps < 1:
        return RedirectResponse("/movie/" + slug)

    download = CONFIG.DOWNLOAD_ENABLED

    f = await crud.get_movie_episode_files( m['id'], season, eps)
    return templates.TemplateResponse("movie_parts.html", {
        "request": request,
        'mov'   : m,
        'title' : f'{ m["title"] } S{season} E{eps}' ,
        'res'   : f,
        'dwld'  : download
    })

@router.get("/{slug}/s{season}")
async def get_series_seasons(request: Request, slug:str, season:int):
    m = await crud.get_series_by_slug( slug)

    if not m or not m['is_series']:
        raise HTTPException(404, "Page not found")

    if season < 1:
        return RedirectResponse("/movie/" + slug)
    # pr
    c = await crud.get_genre_matches( m['genre'])
    s = await crud.get_movie_seasons( m['id'])

    e = await crud.get_movie_episodes( m['id'], season)

    return templates.TemplateResponse("movie_season.html", {
        "request": request,
        'mov'   : m,
        'ses'   : s,
        'cses'  : season,
        'ctg'   : c,
        'eps'   : e
    })


@router.get("/{slug}")
async def get_series_by_name(request: Request, slug:str):
    m = await crud.get_series_by_slug( slug)

    if not m or not m['is_series']:
        raise HTTPException(404, "Page not found")

    # pr
    c = await crud.get_genre_matches( m['genre'])
    
    s = await crud.get_movie_seasons( m['id'])
    
    # return m
    return templates.TemplateResponse("movie.html", {
        "request": request,
        'movie' : m,
        'seasons' : s,
        'genre' : c
    })

@router.get("")
async def get_series(request: Request, page:int = 1):
    if page < 1:
        page = 1
    m = await crud.get_series( (page-1)*CONFIG.MAX_ITEMS_PER_PAGE, CONFIG.MAX_ITEMS_PER_PAGE)
    return templates.TemplateResponse("movies.html",
        {"request": request,'title' : 'Series','movies' : m,'page':page})

