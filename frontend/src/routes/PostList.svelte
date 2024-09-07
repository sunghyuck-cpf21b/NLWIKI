<script>
    import {fastapi} from "../lib/api"
    import { link, push } from 'svelte-spa-router'    // href 앞에 link 를 사용하면 주소에 # 이 붙어 하나의 페이지로 인식된다.
    import { page, now_page, T_page, is_login } from "../lib/store"
    import SideBar from "../components/Side_Bar.svelte";

    import moment from 'moment/min/moment-with-locales'
    moment.locale('ko')

    import * as myurl from "../lib/myurl"
    
    if(!$is_login) {
        push(myurl.userlogin_url)
    }

    let post_list = [] 
    let total = 0
    let size = 10
    let kw = ''


    $: total_page = Math.ceil(total/size)

    function get_post_list(_page) {
        
        let params = {
            page: _page,
            size: size,
            keyword: kw,
        }

        fastapi('get', '/api/post/list', params, (json) => {
            post_list = json.post_list
            $page = _page 
            total = json.total
        })
        
    }
  
    $: get_post_list($page)


    
</script>

<section>
    <div class='post_table'>
        <div class='tool_bar'>

            <a class='create_post {$is_login ? '' : 'disabled'}' use:link href={myurl.postcreate_url}>논란 작성</a>

        </div>
        <table>
            <thead>
                <tr>
                    <th class='th-id'>논란번호</th>
                    <th class='th_person'>주요 인물</th>
                    <th class='th-subject'>제목</th>
                    <th>작성자</th>
                    <th>발생일</th>
                    <th>작성일</th>
                </tr>
            </thead>
            <tbody>
                {#each post_list as post}
                    <tr>
                        <td>{post.id}</td>
                        <td>{post.person}</td>
                        <td style='text-align: left;'>
                            <a use:link href={myurl.postdetail_url+'/'+post.id}>{post.subject}</a>
                            {#if post.comments.length > 0}
                            <span> 
                                [{post.comments.length}]
                            </span>
                            {/if}
                        </td>
                        <td>{post.user ? post.user.username : ''}</td>
                        <td class='th_date'>{moment(post.occ_date).format("YYYY.MM.DD")}</td>
                        <td class='th_date'>{moment(post.create_date).format('YYYY.MM.DD')}</td>
                    </tr>
                {/each}
            </tbody>
        </table>    
        <!-- page -->
        <div class='page_room'>
            <p class='page_shift'>
                {#if $T_page > 0}
                    <a class='page_shift' href='/' on:click|preventDefault={()=>{($T_page-=1); get_post_list($T_page*5); ($now_page=$T_page*5+1)}}>이전</a>
                {/if}
            </p>
            <div class='page_box'>
            {#each [1,2,3,4,5] as n}
                <p class='page_num'>
                {#if $T_page*5+n <= total_page}
                    {#if $T_page*5+n === $now_page}
                        <a style='text-decoration-line: underline; font-weight: 600;' href='/' on:click|preventDefault={()=>{get_post_list($T_page*5+n-1); ($now_page=$T_page*5+n);}}>{$T_page*5+n}</a>
                    {:else}
                        <a href='/' on:click|preventDefault={()=>{get_post_list($T_page*5+n-1); ($now_page=$T_page*5+n);}}>{$T_page*5+n}</a>
                    {/if}
                {/if}
                </p>
            {/each}
            </div>
            <p class='page_shift'>
                {#if $T_page*5+5 < total_page}
                    <a href='/' on:click|preventDefault={()=>{($T_page+=1); get_post_list($T_page*5); ($now_page=$T_page*5+1)}}>다음</a>
                {/if}
            </p>
        </div>
    </div>
</section>

<aside>
    <SideBar />
</aside>


<style> 

    .post_table {
        width: 800px;
        margin: 0 auto;
        font-size: 14px;
        padding-bottom: 10px;
    }

    .tool_bar {
        position: relative;
        height: 40px;
    }

    a.create_post {
        position: absolute;
        right: 0px;
        top: 50%;
        transform: translate(0, -50%);
        border: 1px solid #000000;
        padding: 1px 5px;
        font-size: 15px;
    }

    a.create_post:hover {
        text-decoration: none;
    }

    a {
        text-decoration-line: none;
        color: #000000;
    }

    a:hover {
        text-decoration: underline;
    }

    table {
        width: 100%;
        margin: 10px auto;
        text-align: center;
    }

    .th-id {
        width: 10%;
    }

    .th-subject {
        width: 60%
    }

    .th_person {
        width: 15%
    }

    .th_date {
    }

    tbody tr:hover {
        background-color: #f3f3f3;
    }

    tr {
        border-bottom: 1px solid #dddddd;
    }

    th {
        border-top: 4px solid #000000;
        border-bottom: 2px solid #000000;
    }

    td, th {
        padding: 0 3px;
    }

    .page_room {
        margin: 0 auto;
        min-width: 300px;
        height: 25px;
        display: flex;
        justify-content: center;
    }
    .page_box {
        min-width: 200px;
        display: flex;
        justify-content: space-evenly;
    }

    .page_shift {
        width: 30px;
    }

    .page_num {
        margin: 0 auto;
        min-width: 10px;
    }

</style>
