<script>
    import fastapi from "../lib/api"
    import { link, push } from 'svelte-spa-router'    // href 앞에 link 를 사용하면 주소에 # 이 붙어 하나의 페이지로 인식된다.
    import { page, now_page, T_page, is_login } from "../lib/store"

    import moment from 'moment/min/moment-with-locales'
    moment.locale('ko')
    
    if(!$is_login) {
        push('/user-login')
    }

    let nonlan_list = [] 
    let total = 0
    let size = 10
    let kw = ''


    $: total_page = Math.ceil(total/size)

    function get_nonlan_list(_page) {
        
        let params = {
            page: _page,
            size: size,
            keyword: kw,
        }

        fastapi('get', '/api/nonlan/list', params, (json) => {
            nonlan_list = json.nonlan_list
            $page = _page 
            total = json.total
        })
        
    }
  
    $: get_nonlan_list($page)


    
</script>


<div class='nonlan_table'>
    <div class='tool_bar'>

        <a class='create_nonlan {$is_login ? '' : 'disabled'}' use:link href='/nonlan_create'>논란 작성</a>

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
            {#each nonlan_list as nonlan}
                <tr>
                    <td>{nonlan.id}</td>
                    <td>{nonlan.person}</td>
                    <td style='text-align: left;'>
                        <a use:link href='/detail/{nonlan.id}'>{nonlan.subject}</a>
                        {#if nonlan.comments.length > 0}
                        <span> 
                            [{nonlan.comments.length}]
                        </span>
                        {/if}
                    </td>
                    <td>{nonlan.user ? nonlan.user.username : ''}</td>
                    <td class='th_date'>{moment(nonlan.occ_date).format("YYYY.MM.DD")}</td>
                    <td class='th_date'>{moment(nonlan.create_date).format('YYYY.MM.DD')}</td>
                </tr>
            {/each}
        </tbody>
    </table>    
    
    <!-- page -->
    <div class='div_page'>
        {#if $T_page > 0}
            <a class='page_back' href='/' on:click|preventDefault={()=>{($T_page-=1); get_nonlan_list($T_page*5); ($now_page=$T_page*5+1)}}>이전</a>
        {/if}
        {#each [1,2,3,4,5] as n}
            {#if $T_page*5+n <= total_page}
                {#if $T_page*5+n === $now_page}
                    <a class='page_{n}' style='text-decoration-line: underline; font-weight: 600;' href='/' on:click|preventDefault={()=>{get_nonlan_list($T_page*5+n-1); ($now_page=$T_page*5+n);}}>{$T_page*5+n}</a>
                {:else}
                    <a class='page_{n}' href='/' on:click|preventDefault={()=>{get_nonlan_list($T_page*5+n-1); ($now_page=$T_page*5+n);}}>{$T_page*5+n}</a>
                {/if}
            {/if}
        {/each}
        {#if $T_page*5+5 < total_page}
            <a class='page_next' href='/' on:click|preventDefault={()=>{($T_page+=1); get_nonlan_list($T_page*5); ($now_page=$T_page*5+1)}}>다음</a>
        {/if}
    </div>

</div>




<style> 

    .nonlan_table {
        width: 800px;
        margin: 0 auto;
        font-size: 14px;
    }

    .tool_bar {
        position: relative;
        height: 40px;
    }

    a.create_nonlan {
        position: absolute;
        right: 0px;
        top: 50%;
        transform: translate(0, -50%);
        border: 1px solid #000000;
        padding: 1px 5px;
        font-size: 15px;
    }

    a.create_nonlan:hover {
        text-decoration: none;
    }

    a, li > a {
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

    .div_page {
        position: relative;
        width: 70%;
        margin: 15px auto;
    }

    .page_back {
        position: absolute;
        left: 15%;
        transform: translate(50%, 0);
    }

    .page_next {
        position: absolute;
        right: 15%;
        transform: translate(-50%, 0);
    }

    .page_1 {
        position: absolute;
        left: 30%;
        transform: translate(-50%, 0);
    }
    .page_2 {
        position: absolute;
        left: 40%;
        transform: translate(-50%, 0);
    }
    .page_3 {
        position: absolute;
        left: 50%;
        transform: translate(-50%, 0);
    }
    .page_4 {
        position: absolute;
        left: 60%;
        transform: translate(-50%, 0);
    }
    .page_5 {
        position: absolute;
        left: 70%;
        transform: translate(-50%, 0);
    }
</style>
