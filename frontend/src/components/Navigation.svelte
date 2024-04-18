<script>
    import { link } from 'svelte-spa-router'
    import { page, access_token, username, is_login } from "../lib/store"
</script>

<!-- 네비게이션바 -->
<nav>
    <div>
        <a class='go_home' use:link href="/" on:click={()=>{$page=0}}>논란위키</a>
        <!--
        <a class='create_btn' use:link href="/nonlan_create">논란 작성</a>
        -->
        <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation">
        <span class="navbar-toggler-icon" />
    </button>
        <div>
            <ul>
                {#if $is_login}
                    <li>
                        <a use:link href='/user-login' on:click={()=>{
                            $access_token = ''
                            $username = ''
                            $is_login = false
                        }}>로그아웃 ({$username})</a>
                    </li>
                {:else}
                    <li>
                        <a use:link href='/user-create'>회원가입</a>
                    </li>
                    <li>
                        <a use:link href='/user-login'>로그인</a>
                    </li>
                {/if}
            </ul>
        </div>
    </div>
</nav>


<!--
<style>
    nav {
        height: 50px;
        border-bottom: 1px solid #000000;
        /*position: fixed;*/
        display: flex;
        align-items: center;
    }

    nav > div {

    }

    a {
        color: #000000;
        text-decoration-line: none;
    }

    .go_home {
        font-size: 20px;
    }

    .create_btn {
        font-size: 15px;
    }
</style>
-->