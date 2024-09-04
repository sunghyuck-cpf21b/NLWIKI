<script>
    import { push } from 'svelte-spa-router'
    import {fastapi} from '../lib/api'
    import Error from '../components/Error.svelte';

    import * as myurl from "../lib/myurl"

    let error = {detail:[]}
    let username = ''
    let password1 = ''
    let password2 = ''

    function post_user(event) {
        event.preventDefault()
        let url = '/api/user/create'
        let params = {
            username: username,
            password1: password1,
            password2: password2,
        }
        fastapi('post', url, params,
            (json) => {
                push(myurl.userlogin_url)
            },
        (json_error) => {
            error = json_error
        })
    }
</script>

<div>
    <h5>회원 가입</h5>
    <Error error={error} />
    <form method='post'>
        <div>
            <lebel for='username'>사용자 이름</lebel>
            <input type='text' id='username' bind:value='{username}'>
        </div>
        <div>
            <label for='password1'>비밀번호</label>
            <input type='password' id='password1' bind:value='{password1}'>
        </div>
        <div>
            <label for='password2'>비밀번호 확인</label>
            <input type='password' id='password2' bind:value='{password2}'>
        </div>
        <button type='submit' on:click='{post_user}'>생성하기</button>
    </form>
</div>