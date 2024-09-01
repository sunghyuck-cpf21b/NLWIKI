<script>
    import { push } from 'svelte-spa-router'
    import fastapi from '../lib/api'
    import Error from '../components/Error.svelte';
    import { access_token, username, is_login } from '../lib/store'

    let error = {detail:[]}
    let login_username = ''
    let login_password = ''

    async function login(event) {
        event.preventDefault()
        let url = "/api/user/login"
        let params = {
            username: login_username,
            password: login_password,
        }
        console.log('123123123')
        await fastapi('login', url, params,
            (json) => {
                $access_token = json.access_token 
                $username = json.username 
                $is_login = true 
                push('/')
            },
            (json_error) => {
                error = json_error
        })
    }
</script>

<div class='login_box'>
    <h5>로그인</h5>
    <Error error={error} />
    <form method='post'>
        <div class='login_box'>
            <label for='username'>사용자 이름</label>
            <input type='text' id='username' bind:value='{login_username}'>
        </div>
        <div class='login_box'>
            <label for='password'>비밀번호</label>
            <input type='password' id='password' bind:value='{login_password}'>
        </div>
        <button type='submit' on:click='{login}'>로그인</button>
    </form>
</div>


<style>
    .login_box {
        border: 1px solid #000000;
        width: 400px;
        display: flex;
        height: 300px;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    form {
        display: flex;
        flex-direction: column;
        height: 200px;
        justify-content: space-evenly;
        align-items: center;
    }
</style>