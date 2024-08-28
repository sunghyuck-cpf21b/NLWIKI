import fastapi from "./api"

export function calendar_maker(year, month) {
    let full_date_list = []
    const first_date = new Date(year, month-1, 1)
    const last_date = new Date(year, month, 0)
    const week = Math.ceil((last_date.getDate()+first_date.getDay())/7)
    let start_date 
    if (month === 1) {
        start_date = 32 - first_date.getDay()
    } else {
        start_date = new Date(year, month-1, 0).getDate() - first_date.getDay() + 1
    }
    for (let i=0; i<week; i++) {
        let temp = []
        let temp_full = []
        for (let j=0; j<7; j++) {
            let date = i*7+j + start_date 
            let FULL
            if (date < start_date+first_date.getDay()) {
                if (month === 1) {
                    FULL = `${year-1}-12-${date}`
                } else if (10<month) {
                    FULL = `${year}-0${month-1}-${date}`
                } else {
                    FULL = `${year}-0${month-1}-${date}`
                }
            } else if (start_date+first_date.getDay() <= date && date < start_date+first_date.getDay()+last_date.getDate()) {
                const temp_date = date-start_date-first_date.getDay()+1
                let full_month=month; let full_date=temp_date
                if (month < 10) {full_month = `0${month}`}
                if (temp_date < 10) {full_date = `0${temp_date}`}
                FULL = `${year}-${full_month}-${full_date}`

            } else {
                const temp_date = date-start_date-first_date.getDay()-last_date.getDate()+1
                let full_month = month+1
                if (month+1 < 10) {full_month = `0${month+1}`}
                if (month === 12) {
                    FULL = `${year+1}-01-0${temp_date}`
                } else {
                    FULL = `${year}-${full_month}-0${temp_date}`
                }
            }
            temp_full.push(FULL)
        }
        full_date_list.push(temp_full)
    }
    return full_date_list
}




async function num_to_str(num_list) {
    let list = []
    for (const num of num_list) {
        list.push(String(num).padStart(2, '0'))
    }
    return list
}

async function start_end(year, month) {
    const start_day = new Date(year, month-1, 1).getDay()
    const end_day = new Date(year, month, 0).getDay()
    
    const start_date = new Date(year, month-1, 1-start_day)
    const last_date = new Date(year, month, end_day)
    
    const num_list  = [start_date.getMonth()+1, start_date.getDate(), last_date.getMonth()+1, last_date.getDate()]
    const str_list = await num_to_str(num_list)

    const start_str = `${start_date.getFullYear()}-${str_list[0]}-${str_list[1]}`
    const end_str = `${last_date.getFullYear()}-${str_list[2]}-${str_list[3]}`
    return [start_str, end_str]
}

// 월간 프로그램 데이터 가져오기
export async function get_month_data_2(year, month, username) {
    const start_and_end = await start_end(year, month)
    const url = '/api/sep_program/month_data_2'
    const params = {
        start_date: start_and_end[0],
        end_date: start_and_end[1],
        username: username,
    }
    let data = []
    let bool
    await fastapi('get', url, params, 
        (json)=>{
            data = json 
            bool = true
        }
    )
    return [data, bool]
}

// 한달 주간 메모 가져오기
export async function get_month_weekly_memo(year, month, username) {
    const start_and_end = await start_end(year, month)
    const url = '/api/weeklymemo/month_memo'
    const params = {
        start_date: start_and_end[0],
        end_date: start_and_end[1],
        username: username,
    }
    let data = []
    let bool
    await fastapi('get', url, params,
        (json)=>{
            data = json 
            bool = true
        }
    )
    return [data, bool]
}
// 단일 주간 메모 가져오기
export async function get_weekly_memo(date, username) {
    const url = '/api/weeklymemo/memo'
    const params = {
        date: date,
        username, username
    }
    let data = {}
    await fastapi('get', url, params,
        (json)=>{
            data = json
        }
    )
    return data
}

// 주간 메모 생성 및 수정
export async function post_weekly_memo(sunday_date, content, data) {
    let url = '/api/weeklymemo/create'
    let operation = 'post'
    console.log(sunday_date)
    if (data[sunday_date]) {
        url = '/api/weeklymemo/update'
        operation = 'put'
    }
    const params = {
        sunday_date: sunday_date,
        content: content,
    }
    let edit_complete = false
    await fastapi(operation, url, params,
        (json)=>{
            edit_complete = true
        }
    )
    return edit_complete 
}
// 주간 메모 삭제
export async function delete_weekly_memo(sunday_date) {
    const url = '/api/weeklymemo/delete'
    const params = {
        sunday_date: sunday_date,
    }
    let edit_complete = false
    await fastapi('delete', url, params,
        (json)=>{
            edit_complete = true
        }
    )
    return edit_complete
}


export async function get_month_data(year, month) {
    const url = '/api/sep_program/month_data'
    const params = {
        year: year,
        month: month
    }
    let month_data = {}
    let bool;
    await fastapi('get', url, params,
        (json)=>{
            month_data = json 
            bool = true
        }
    )
    return [month_data, bool]
}

