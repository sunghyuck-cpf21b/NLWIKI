import { fastapi } from "./api"

export async function get_categories({task}) {
    const url = '/api/post/categories'
    const params = {
        task: task
    }
    let data = []
    await fastapi('get', url, params,
        (json)=>{
            data = json
        }
    )
    return data
}