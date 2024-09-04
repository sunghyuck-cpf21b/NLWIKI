<script>
    import { push } from 'svelte-spa-router'
    import {fastapi} from "../lib/api"
    import Error from '../components/Error.svelte'

    let error = {detail:[]}

    let file;
    let filename = []
    let fileurl = []

    function temp_img(event) {

        event.preventDefault()
        let url = "/api/file/temp_upload"
        let params = {
            file: file
        }
        fastapi('post', url, params,
            (json) => {
                filename = filename,
                fileurl = fileurl
            })
    }
</script>


<p>test</p>