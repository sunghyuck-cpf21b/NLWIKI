<script>
    import {fastapi} from '../lib/api'
    import Error from '../components/Error.svelte'
    import { link, push } from 'svelte-spa-router'
    import { is_login, set_admin, username } from '../lib/store'
    import { marked } from 'marked'
    import moment from 'moment/min/moment-with-locales'  
    import { get } from 'svelte/store';

    import SideBar from '../components/Side_Bar.svelte'
    moment.locale('ko')

    import * as myurl from "../lib/myurl"   

    if(!$is_login) {
        push(myurl.userlogin_url)
    }

    //const split_code = 'split_subuncream_point'
    export let params = {}
    // App.svelte에서 호출할 때 params를 읽어야 하므로 export를 이용해 변수를 선언한다.
    let post_id = params.post_id 
    // 위키독스 설명 : Detail 컴포넌트를 호출할 때 파라미터 값이 전달된다. (Home.svelte에서 전달되는지, App.svelte에서 전달되는지, 아니면 Home->App->Detail 순서로 전달되는지 잘 모르겠음)

    // 이 파일에서만 본다면 params에는 아무 속성도 작성되지 않았지만 
    // App.svelte에서 Router 클래스에 의해 불러진 이후에 params값이 정의되기 때문에 post_id의 속성을 정할 수 있게 되는 것이다.
    /* 각 컴포넌트들은 App.svelte 에서 사용될 함수와 같은 코드를 작성해준다고 생각하면 편하다 */
    let post = {comments: [], content: '', person: '', occ_date: '', user: ''}

    /*비동기 방식의 문제(데이터 로드 전에 ui 실행, 보호 매커니즘이 있지만 여러 표현방식을 사용하다보면 문제 발생 가능) 
    때문에 post 딕셔너리의 속성에 불러와지는 값 들을 초기화 해준다고 하지만
    그냥 불러오는 데이터에 있는 모든 속성들을 해주는게 마음이 편할듯 */
    let comment_content = ''
    let subcomment_content = ''
    let error = {detail:[]}
    
    function get_post() {
        fastapi("get", "/api/post/detail/"+post_id, {}, (json) => {
            post = json
            console.log(json)
        }) // params 매개변수에 값을 넣지 않는 이유는 백엔드의 router데코레이터 url의 가변형 변수가 자동적으로 id값에 매칭되기 때문이다.
    }

    get_post()

    function delete_post(_post_id) {
        if(window.confirm('정말로 삭제하시겠습니까?')) {
            let url = '/api/post/delete'
            let params = {
                post_id: _post_id
            }
            fastapi('delete', url, params,
                (json) => {
                    console.log(myurl.postlist_url)
                    push(myurl.postlist_url)
                },
                (err_json) => {
                    error = err_json
                })
        }
    }

    function post_comment(event) {
        event.preventDefault()
        let url = '/api/comment/create/' + post_id
        let params = {
            content: comment_content
        }
        fastapi('post', url, params, 
            (json)=>{
                comment_content = ''
                error = {detail:[]}
                get_post()
            },
            (err_json)=>{
                error = err_json
            })
    }

    function delete_comment(_comment_id) {
        if(window.confirm('정말로 삭제하시겠습니까?')) {
            let url='/api/comment/delete'
            let params = {
                comment_id: _comment_id
            }
            fastapi('delete', url, params,
                (json)=>{
                    get_post()
                },
                (err_json)=>{
                    error = err_json
                })
            }
    }

    async function subcomment_create(comment_id) {
        console.log(subcomment_content)
        const url = '/api/comment/sub/create/'+comment_id
        const params = {
            content: subcomment_content
        }
        await fastapi('post', url, params, 
            (json)=>{
                subcomment_content = ''
                error = {detail:[]}
                subcomment_num = -1
                get_post()
            }, (err_json)=>{
                error = err_json
            }
        )
    }

    async function delete_subcomment(subcomment_id) {
        if(window.confirm('답글을 삭제하시겠습니까?')) {
            const url = '/api/comment/sub/delete'
            const params = {
                data_id: subcomment_id
            }
            await fastapi('delete', url, params, 
                (json)=>{
                    get_post()
                }
            )
        } 
    }


    let subcomment_num = -1
</script>


<section>
    <div class='content_box'>
        <div class='content_info_room'>
            <div class='subject'>
                <span style={post.category==='논란' ? 'color: #ff0000':'#000000'}>[{post.category}]</span> 
                {post.subject}
            </div>
            <div class='content_info_box'>
                <span>작성 정보</span>
                <span class='content_info'>{post.user.username}</span>
                <span class='content_info'>{moment(post.create_date).format("YYYY.MM.DD HH:mm:ss")}</span>
            </div>
            {#if post.category == '논란'}
            <div class='content_info_box'>
                <span>논란 정보</span>
                <span class='content_info' style='color: #ff0000; font-weight: 600;'>{post.person}</span>
                <span class='content_info'>{moment(post.occ_date).format("YYYY.MM.DD")}</span>
            </div>
            {/if}
        </div>
        
        <div class='main_content_box'>
            <div class='main_content'>
                {@html post.content}
            </div>
            {#if post.user && $username === post.user.username}
                <button on:click={()=>delete_post(post_id)}>게시물 삭제</button>
                <button on:click={()=>{push(`/postmodify/${post.id}`)}}>게시물 수정</button>
            {/if}
        </div>
        
        <div class='comment_room'>
            {#each post.comments as comment, i}
                <div class='comment_box'>
                    <div class="comment_user">
                        {comment.user.username}
                    </div>
                    <div class='comment_content'>
                        {@html comment.content}
                    </div>
                    <div class='comment_btn_room'>
                        <div class='comment_date'>
                            {moment(comment.create_date).format("YYYY.MM.DD HH:mm:ss")}
                        </div>
                        <div class='comment_btn_box'>
                            <button class='comment_btn add_sub' on:click={()=>{subcomment_num=i; console.log(subcomment_num)}}>답글</button>
                            {#if comment.user.username === $username}
                            <button class='comment_btn del_com' on:click={()=>delete_comment(comment.id)}>삭제</button>
                            {/if}
                        </div>
                    </div>
                    {#if comment.subcomments.length || subcomment_num === i}
                    <div class='subcomment_room'>
                        {#if subcomment_num === i}
                        <div class='subcomment_create_box'>
                            <div class='comment_div'>
                                <textarea class='comment_textarea' bind:value={subcomment_content}></textarea>
                                <button on:click={()=>{subcomment_create(comment.id)}}>답글 등록</button>
                            </div>
                        </div>
                        {/if}
                        {#each comment.subcomments as subcomment}
                        <div class='subcomment_box'>
                            <div>{subcomment.user.username}</div>
                            <div>{@html subcomment.content}</div>
                            <div class='comment_btn_room'>
                                <div class='comment_date'>
                                    {moment(subcomment.create_date).format("YYYY.MM.DD HH:mm:ss")}
                                </div>
                                <div class='comment_btn_box'>
                                    {#if subcomment.user.username === $username}
                                    <button class='comment_btn del_com' on:click={()=>delete_subcomment(subcomment.id)}>삭제</button>
                                    {/if}
                                </div>
                            </div>
                        </div>
                        {/each}
                    </div>
                    {/if}
                </div>
            {/each}
            <form class='comment_form' method='post'>
                <div class='comment_div'>
                    <textarea 
                    class='comment_textarea'
                    rows='3' bind:value={comment_content} disabled={$is_login ? '' : 'disabled'}></textarea>
                    <input type='submit' value='댓글 등록' class='{$is_login ? '' : 'disabled'}' on:click='{post_comment}'>
                </div>
                
            </form>
        </div>
        
        <button on:click={()=>{push(myurl.postlist_url)}}>목록으로</button>

        <Error error={error} />
    
    </div>
</section>

<aside>
    <SideBar />
</aside>


            <!-- svelte는 비동기적으로 script와 body 부분이 실행된다. 
            하지만 데이터가 로드되기 전에 ui가 실행되는 문제를 방지하는 보호 매커니즘이 내장되어 있기 때문에 
            일반적인 경우에는 undefined가 표시되지 않지만, 표시할 부분에 마크다운이나, 이와 같은 기능이 
            포함되어 있는 경우에는 데이터 로드 전인 post.content를 변환하려고 시도하기 때문에
            공백을 변환하여 undefined가 표시되는 것이다. 
            *데이터가 로드된 후에 리액티브하게 받아오면 좋겠건만...*-->

<!-- 
on:click은 문자열 전달과 함수 전달 방식이 있다.
on:click = {() => 함수(매개변수)} 
on:click = "{문자열 또는 함수"

함수 전달은 클릭 이벤트 발생 시 함수가 실행되지만
문자열 전달은 문자열이 javascript로 평가되어 실행된다.
-->


<style>
    :root {
        --comment-font-size: 13px; 
    }
    .subject {
        font-size: 20px;
        font-weight: 600;
    }
    .content_info_room {

    }
    .content_info_box {
        display: flex;
        font-size: 13px;
    }
    .content_info_box > span {
        
    }
    :global(.content_info::before) { /* svelte 스타일 스코핑 매커니즘으로 인한 잘못된 적용 피하기 위해 global로 설정함 */
        content: '';
        display: inline-block;
        width: 1px;
        height: 12px;
        background: #ccc;
        margin: 0 10px 0 10px;
        vertical-align: -2px;
    }
    .content_info_room::after {
        content: '';
        display: inline-block;
        margin: 0 auto;
        width: 100%;
        height: 1px;
        background-color: #ccc;
    }
    .content_box {
        width: 800px;
    }
    .main_content {
        font-size: 14px;
        margin: 20px auto 50px;
    }


/* comment part */
    .comment_room {
        font-size: var(--comment-font-size);
        width: 100%;
        margin: 20px auto;
        padding: 10px 0;
        border: 3px solid #000000;
        border-left: none;
        border-right: none;
    }

    .comment_box {
        position: relative;
        border-bottom: 1px solid #000000;
    }
    .comment_box, .subcomment_box {
        display: grid;
        width: 100%;
        grid-template-columns: 120px 1fr 125px;
        grid-template-areas: 
        "a b c"
        'd d d';
        align-items: center;
        padding: 5px 10px;
    }
    .comment_btn_room {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        justify-content: flex-start;
    }
    .comment_btn {
        display: inline;
        font-size: 11px;
    }
    .subcomment_room {
        grid-area: d;
        position: relative;
        margin: 10px 0 5px 30px;
        border: 1px solid;
        border-top: none;
    }
    .subcomment_box, .subcomment_create_box {
        border-top: 1px solid;
        margin: 0;
        width: 100%;
    }
    .subcomment_create_box {
        height: 110px;
    }

    .comment_info {
        grid-area: a;
    }
    .comment_content {
        grid-area: b;
    }
    .comment_date {
        position: static;
        grid-area: c;
        opacity: 0.5;
    }
    .comment_form {
        margin: 10px auto;
    }
    .comment_div {
        padding: 5px;
        width: 95%;
        height: 110px;
        margin: 0 auto;
    }
    .comment_textarea {
        background-color: var(--main-bg-color);
        width: 100%;
        height: 60%;
        margin: 0 auto;
        color: #000000;
    }

</style>