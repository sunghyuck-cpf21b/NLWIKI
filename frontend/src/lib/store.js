import { writable } from "svelte/store";

const persist_storage = (key, initValue) => {
    const storedValueStr = localStorage.getItem(key)
    const store = writable(storedValueStr != null ? JSON.parse(storedValueStr) : initValue)
    // 물음표 조건문 => 조건 ? true return : false return
    store.subscribe((val) => {
        localStorage.setItem(key, JSON.stringify(val))
    })
    return store
}

export const page = persist_storage("page", 0)
export const now_page = persist_storage("now_page", 1)
export const T_page = persist_storage("T_page", 0)

let NowDay = new Date
const ST_year = NowDay.getFullYear()
const ST_month = NowDay.getMonth()+1
export const year = persist_storage("year", ST_year)
export const month = persist_storage("month", ST_month)

export const access_token = persist_storage("access_token", "")
export const username = persist_storage("username", "")
export const is_login = persist_storage("is_login", false) 
export const set_admin = persist_storage("ser_admin", false)
