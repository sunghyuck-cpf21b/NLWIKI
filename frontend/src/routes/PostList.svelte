<script>
    import {fastapi} from "../lib/api"
    import { link, push } from 'svelte-spa-router'    // href 앞에 link 를 사용하면 주소에 # 이 붙어 하나의 페이지로 인식된다.
    import { page, now_page, T_page, is_login } from "../lib/store"
    import SideBar from "../components/Side_Bar.svelte";
    import * as api_funcs from '../lib/api_funcs'

    import moment from 'moment/min/moment-with-locales'
    moment.locale('ko')

    import * as myurl from "../lib/myurl"



    if(!$is_login) {
        push(myurl.userlogin_url)
    }

    console.log('now_page=', $now_page,'T_page=', $T_page)

    let post_list = [] 
    let total = 0
    let size = 20
    let kw = ''

    let notification_list = []
    let notification_size = 10

    $: total_page = Math.ceil(total/size)

    let categories = []
    let selected_category = '전체'

    api_funcs.get_categories({task:'list'}).then(data=>{
        categories = data
    })

    async function get_post_list(PG, size, kw, category) {
        let params = {
            page: PG,
            size: size,
            keyword: kw,
            category: category,
        }
        let post_list = []; let _page; let total;
        await fastapi('get', '/api/post/list', params, (json) => {
            post_list = json.post_list
            _page = PG
            total = json.total
        })
        return [post_list, _page, total]
    }
    $: get_post_list($now_page, size, kw, selected_category).then(data=>{
        post_list = data[0]
        total = data[2]
    })


    get_post_list(0, notification_size, '', '공지').then(data=>{ // 공지 가져오기
        notification_list = data[0]
    })
    
</script>

<section>
    <div class='post_table'>
        <div class='tool_bar'>
            <select class='select_category' on:change={()=>{selected_category=event.target.value}}>
                {#each categories as c}
                <option style={(c=='논란') ? 'color: #ff0000':''}>{c}</option>
                {/each}
            </select>
            <a class='create_post {$is_login ? '' : 'disabled'}' use:link href={myurl.postcreate_url}>게시글 작성</a>

        </div>
        <table>
            <thead>
                <tr>
                    <th class='th-id'>번호</th>
                    <!--<th class='th_person'>주요 인물</th>-->
                    <th class='th-subject'>제목</th>
                    <th>작성자</th>
                    <!--<th>발생일</th>-->
                    <th>작성일</th>
                </tr>
            </thead>
            <tbody>
                {#each notification_list as note}
                <tr>
                    <td>{note.id}</td>
                    <td style='text-align: left;'>
                        <a use:link href={myurl.postdetail_url+'/'+note.id}>
                            <span class='category' style='color: #000000; font-weight: 600;'>[{note.category}]&nbsp;&nbsp;</span>
                            {note.subject}
                        </a>
                        {#if note.comments.length > 0}
                        <span> 
                            [{note.comments.length}]
                        </span>
                        {/if}
                    </td>
                    <td>{note.user ? note.user.username : ''}</td>
                    <td class='th_date'>{moment(note.create_date).format('YYYY.MM.DD')}</td>
                    
                </tr>
                {/each}
                {#each post_list as post}
                <tr>
                    <td>{post.id}</td>
                    <!--<td>{post.person}</td>-->
                    <td style='text-align: left;'>
                        <a use:link href={myurl.postdetail_url+'/'+post.id}>
                            {#if post.category=='공지'}
                            <span class='category' style='color: #000000; font-weight: 600;'>[{post.category}]&nbsp;&nbsp;</span>
                            {:else if post.category=='논란'}
                            <span class='category' style='color: #ff0000; font-weight: 600;'>[{post.category}]&nbsp;&nbsp;</span>
                            {:else}
                            <span class='category'>[{post.category}]&nbsp;&nbsp;</span>
                            {/if}
                            
                            {post.subject}
                        </a>
                        {#if post.comments.length > 0}
                        <span> 
                            [{post.comments.length}]
                        </span>
                        {/if}
                    </td>
                    <td>{post.user ? post.user.username : ''}</td>
                    <!--<td class='th_date'>{moment(post.occ_date).format("YYYY.MM.DD")}</td>-->
                    <td class='th_date'>{moment(post.create_date).format('YYYY.MM.DD')}</td>
                </tr>
                {/each}
            </tbody>
        </table>    
        <!-- page -->
        <div class='page_room'>
            <p class='page_shift'>
                {#if $T_page > 0}
                    <a class='page_shift' href='/' on:click|preventDefault={()=>{($T_page-=1);($now_page=$T_page*5+1)}}>이전</a>
                {/if}
            </p>
            <div class='page_box'>
            {#each [1,2,3,4,5] as n}
                <p class='page_num'>
                {#if $T_page*5+n <= total_page} <!-- 게시물 범위를 넘지 않기 위한 장치 -->
                    {#if $T_page*5+n === $now_page}
                        <a style='text-decoration-line: underline; font-weight: 600;' href='/' on:click|preventDefault={()=>{($now_page=$T_page*5+n);}}>{$T_page*5+n}</a>
                    {:else}
                        <a href='/' on:click|preventDefault={()=>{($now_page=$T_page*5+n);}}>{$T_page*5+n}</a>
                    {/if}
                {/if}
                </p>
            {/each}
            </div>
            <p class='page_shift'>
                {#if $T_page*5+5 < total_page}
                    <a href='/' on:click|preventDefault={()=>{($T_page+=1); ($now_page=$T_page*5+1)}}>다음</a>
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
    .select_category {
        position: absolute;
        left: 0px;
        top: 50%;
        transform: translate(0, -50%);
    }
    .select_category > option {
        font-weight: 600;
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

    .category {
        color: #999999;
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
