<script>
    import { fastapi, fileapi } from "../lib/api";
    import { link, push } from 'svelte-spa-router'

    import * as myurl from "../lib/myurl"
    import Error from "../components/Error.svelte";

    const fd = new FormData()
    fd.append('test', '1234567890')


    let imagefile
    let error = {}
    function test(file) {
        if (!file) {
            return
        }
        fd.append('file', file)
        console.log('formdata 조회')
        for (const i of fd) {
            console.log(i)
        }
        const url = '/api/test/img_test'
        const params = fd
        console.log('fastapi 호출 직전', fd)
        fileapi(url, params, 
            (json) => {
                console.log(json)
            }
        )
    }
/*
    let res_html 
    function back_html() {
        const url = '/api/test/html/hahaha'
        console.log(url)
        fastapi('get', url, {},
            (json)=>{
                res_html = json
                console.log(res_html)
            }
        )
    }
    back_html()*/
</script>

<div class='main_home'>    
    <Error error={error}/>
    <!--
    <input id='' type='file' accept="image/*" on:change={(e)=>{imagefile = e.target.files[0]}}>
    <button on:click={()=>{test(imagefile)}}>upload</button>
    -->

    임시 메인 홈 입니다.

    <a use:link href={myurl.postlist_url}>위키 이동</a>

    <!--
    <a href='/media'>media</a>
    -->


    <img src='https://nlwk.nlwiki.com/media/maxresdefault.jpg' alt='' style='width: 100%;'>
    <!--
    {#if res_html}
    {@html res_html}
    {/if}
    -->
</div>

<style>
    .main_home {
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
</style>