import { is_login } from "./store"
import { push } from "svelte-spa-router"

const login_is_main=()=>{
    if(!$is_login) {
        push('/user-login')
    }
}

export default login_is_main