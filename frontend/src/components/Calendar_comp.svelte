<script>
    import {fastapi} from "../lib/api";
    import { link, push } from 'svelte-spa-router'
    import { year, month } from "../lib/store";
    import { findBestMatch } from 'string-similarity';
    import { onMount } from "svelte";
    import { slide } from "svelte/transition";
    import * as caldata from "../lib/caldata";
    import * as my_func from "../lib/my_func"
    import { username, is_login } from "../lib/store";

    // 컴포넌트 외부 입력 변수
    export let params = {}
    let p_username = params.username

    let edit_auth = Boolean(is_login && $username == params.username)
    $: calendar = caldata.calendar_maker(params.year, params.month)
/*
    let month_data = {}
    let data_ready = false
    caldata.get_month_data(params.year, params.month).then(data=>{
        month_data = data[0]
        data_ready = data[1]
    })*/
    
    async function get_daily_data({date, btn_action}) {
        const url = '/api/sep_program/program_date'
        const params = {
            program_date: date
        }
        if (btn_action) {month_data_2[date] = []} // => contenteditable로 인한 태그 내용 복사 방지를 위함, 
        await fastapi('get', url, params,
            (json)=>{
                month_data_2[date] = json.exercises
            }
        )
    }
    

    let month_data_2 = {}
    let data_ready_2 = false
    async function get_MD(year, month, username) {
        await caldata.get_month_data_2(year, month, username).then(data=>{
            data_ready_2 = data[1]
            for (const t of data[0]) {
                month_data_2[t.date] = t.exercises
            }
        })
    }
    $: get_MD(params.year, params.month, p_username)
    

    // weekly_memo
    let month_weekly_memo = {}
    let weekly_memo_ready = false 
    async function get_MWM(year, month, username) {
        await caldata.get_month_weekly_memo(year, month, username).then(data=>{
            weekly_memo_ready = data[1]
            for (const t of data[0]) {
                month_weekly_memo[t.sunday_date] = t.content
            }
        })
    }
    $: get_MWM(params.year, params.month, p_username)

    // memo create/update도 blur 기능으로 실행시키기
    async function weekly_memo_edit(date, content, memo_data, username) {
        let edit_complete = false
        if (content.replace(/\s+/g, '')) { // 메모에 내용이 남아있다면, 생성 또는 수정
            await caldata.post_weekly_memo(date, content, memo_data).then(bool=>{edit_complete = bool})
            if (edit_complete) {
                await caldata.get_weekly_memo(date, username).then(data=>{
                    month_weekly_memo[date] = ''
                    month_weekly_memo[date] = data.content
                    console.log(month_weekly_memo)
                })
            }
        }
        else if (month_weekly_memo[date]) { // 메모가 비어있는채로 실행된다면 삭제 실행
            await caldata.delete_weekly_memo(date).then(bool=>{edit_complete = bool})
            if (edit_complete) {
                delete month_weekly_memo[date]
                month_weekly_memo = { ...month_weekly_memo}
            }
        }
    }
    async function weekly_memo_BL(date) {
        const content = event.target.innerHTML
        weekly_memo_edit(date, content, month_weekly_memo, p_username)
    }

    // sep_program_data
    async function update_data(id, ex_or_vol, key, date, content) { // on_BL 함수 본체, exercise, volume 데이터 수정
        const update_data = content.trim()
        console.log(update_data)
        const url = `/api/sep_program/update/${ex_or_vol}`
        const params = {
            id: id,
            key: key,
            update_data: update_data,
        }

        await fastapi('put', url, params,
            async (json)=>{
                await get_daily_data({date:date})
            }
        )
    }
    async function on_BL(id, ex_or_vol, key, date) { // program 수정 함수, blur 시에 실행됨
        const content = event.target.textContent
        await update_data(id, ex_or_vol, key, date, content)
    }


    async function init_create(event, date) { // 프로그램 임시 생성
        const data = await create_program_date(date)
    }


    async function create_program_date(date) { // 날짜 데이터 생성
        const url = '/api/sep_program/create/program_date'
        const params = { 
            date: date
        }
        await fastapi('post', url, params,
            async (json)=>{
                await get_daily_data({date:date, btn_action:true})
            }
        )
    }
    async function delete_program_date(date) { // 날짜 데이터 삭제
        console.log(date)
        if (Object.keys(month_data_2).includes(date)) {
            if (window.confirm(date+' 의 프로그램을 삭제하시겠습니까?')) {
                const url = '/api/sep_program/delete/program_date'
                const params = {
                    date: date
                }
                await fastapi('delete', url, params)
            }
            delete month_data_2[date]
            month_data_2 = { ...month_data_2}
        }
    }

    async function create_exercise(date, order) { // 운동 데이터 생성
        const url = '/api/sep_program/create/exercise'
        const params = {
            date: date,
            exercise: '',
            order: order
        }
        await fastapi('post', url, params,
            async (json)=>{
                await get_daily_data({date:date, btn_action:true})
            }
        )
    }
    async function delete_exercise(date, exercise_id) { // 운동 데이터 삭제
        const url = '/api/sep_program/delete/exercise'
        const params = {
            exercise_id: exercise_id 
        }
        await fastapi('delete', url, params,
            async (json)=>{
                await get_daily_data({date:date, btn_action:true})
            }
        )
    }

    let basic_weight_kind = 'kg'
    async function create_volume(date, exercise_id) { // 볼륨 데이터 생성
        const url = '/api/sep_program/create/volume'
        const params = {
            exercise_id: exercise_id,
            set: '',
            rep: '',
            weight: '',
            weight_kind: basic_weight_kind
        }
        await fastapi('post', url, params,
            async(json)=>{
                await get_daily_data({date:date})
            }
        )
    }
    function delete_volume(date, exercise_order) {  // 볼륨 데이터 삭제
        const url = '/api/sep_program/delete/volume'
        const volume_data = month_data_2[date][exercise_order]['volumes']
        if (volume_data.length <= 1) {return}
        const volume_id = volume_data[volume_data.length-1].id
        const params = {
            volume_id: volume_id 
        }
        console.log(123333)
        fastapi('delete', url, params, 
            async(json)=>{
                await get_daily_data({date:date})
            }
        )
    }

    async function create_box(date, info, order) { // 운동 + 볼륨 데이터 박스 만들기
        const data = await create_exercise(date, order+1)
    }

    function delete_box(date, info, order) { // 특정 exercise와 연관된 volume도 삭제
        if (month_data_2[date].length === 1) {
            delete_program_date(date)
            return 
        }
        delete_exercise(date, info.id)
    }


    function index_list_maker(MD) {  // 여러 기능을 위한 인덱스 번호 생성기
        const date_list = Object.keys(MD)
        let result = {}
        for (const date of date_list) {
            let cell = -1
            let row = -1
            MD[date].forEach((ex, i)=>{
                cell ++
                row ++
                result[`cell_${date}_${i}_n`] = cell 
                result[`row_${date}_${i}_n`] = row
                ex['volumes'].forEach((v, j)=>{
                    row ++
                    result[`row_${date}_${i}_${j}`] = row
                    for (let k=0; k<3; k++) {
                        cell ++
                        result[`cell_${date}_${i}_${j*3+k}`] = cell 
                    }
                })
            })
            result[`${date}_last_row`] = row
            result[`${date}_last_cell`] = cell
        }
        return result
    }
    $: num_index = index_list_maker(month_data_2)

    let all_ex = []
    function get_all_exercise() { // 현재 저장된 모든운동이름 가져오기 (username 매개변수 추가하기)
        const url = '/api/sep_program/all_ex'
        fastapi('get', url,{},
            (json)=>{
                all_ex = json
            }
        )
    }

    function memo_setting() { // 메모 작성이 정상적으로 작동하게 만들기 위함 함수
        let tag = event.target 
        let key = event.key 
        if (key === 'Enter') {
            event.preventDefault()
            document.execCommand('insertLineBreak')
            console.log(event.target)
        }
        
    }
// ===========================================================================================================================
// ===========================================================================================================================
// ===========================================================================================================================
// ===========================================================================================================================
// ===========================================================================================================================
// ===========================================================================================================================
// ===========================================================================================================================
// ===========================================================================================================================


    let cal = []
    let exercise = []; let volume = []; let memo = []    

    let daily_memo = []
    let cal_bool = []
    let cal_bool_i, cal_bool_j;
    let cal_date;
    let program_bool_i, program_bool_j;
    const NowDay = new Date 
    const NowMonth = NowDay.getMonth()+1
    const today = NowDay.getDate()
    let test_cal = []

    const date_init = new Date
    const year_init = date_init.getFullYear()
    const month_init = date_init.getMonth()+1

    let DD = ['일', '월', '화', '수', '목','금', '토']

    $: rows = cal.length

    let isit_called = false
    let test_var











/*
    let exercise = [] ; let volume = []; let memo = [];
    $: if (cal_program[0]) {        // [주차][요일][운동순서][0:이름, 1:세트, 2:횟수, [3][0]:중량]
        exercise = []; volume = []; memo = [];
        for (let w=0; w<rows; w++) {    // w : week
            let w_exercises = []; let w_volume = []; let w_memo = [];
            for (let d=0; d<7; d++) {   // d : day
                let d_exercises = []; let d_volume = []; let d_memo = [];
                if (cal_program[w][d] !== []) {
                    for (let e of cal_program[w][d]) {
                        d_exercises.push(e[0])
                        d_volume.push(e[1])
                        d_memo.push(e[2])
                    }
                }else {
                    d_exercises.push([])
                    d_volume.push([])
                    d_memo.push([])
                }
                w_exercises.push(d_exercises)
                w_volume.push(d_volume)
                w_memo.push(d_memo)
            }
            exercise.push(w_exercises)
            volume.push(w_volume)
            memo.push(w_memo)
        }
        console.log(volume)
    } */

    let post_day;
    // 프로그램 생성 함수
    function post_program(pd, isit_p, EM, DM) {  // 날짜, 기존 데이터 존재 여부, 
        event.preventDefault()
        const fff = document.getElementById('CP')   //  form 태그
        const ddd = fff.querySelectorAll('.program_input')  // form 태그 바로 하위의 div 태그
        let total_program = []
        for (let d of ddd) {    // 여기서 자동으로 program 형식에 맞게 재가공됨
            let iii = d.querySelectorAll('input')
            let s = d.querySelector('select')
            //  [운동 이름, 세트 수, 횟수, [중량, 중량 종류], [일일 메모]]
            let each_exercise = []
            // 중량값 유뮤에 따라 중량 종류 데이터에 포함시킬지 여부 결정
            if (iii[3].value) {each_exercise = [iii[0].value, iii[1].value, iii[2].value, [iii[3].value, s.value], []]}
            else {each_exercise = [iii[0].value, iii[1].value, iii[2].value, [iii[3].value, ''], []]}
            
            if (iii[0].value !== '') {total_program.push(each_exercise)}
        }   
        let url = '/api/program/create'
        let operation = 'post'
        let params = {  
            program: total_program,
            daily_memo: DM,
            date: pd
        }
        if (isit_p.length!==0) {     // 해당 날짜의 기존 데이터가 존재하면 create -> update 로 변경ㅂ
            url = '/api/program/update'
            operation = 'put'
            if (total_program === []) {
                url = '/api/program/delete'
                operation = 'delete'
            }
        }
        fastapi(operation, url, params,
            (json)=>{
                location.reload()
            },
            (json_error)=>{
                error=json_error
            }
        )
    }

    function delete_program(pd) {
        if (window.confirm(pd+' 의 프로그램을 삭제하시겠습니까?')) {
            event.preventDefault()
            let url = '/api/program/delete'
            let params = {
                program_date: pd
            }
            fastapi('delete', url, params,
                (json)=>{
                    location.reload()
                },
                (json_error)=>{
                    error=json_error
                }
            )
        }
    }


    function date_to_index(date) {
        for (let i=0; i<cal.length; i++) {
            if (cal[i].includes(date)) {
                return [i, cal[i].indexOf(date)]
            }
        }
    }


    //


    // 자동완성을 위해 아래 코드들을 완성해야함




    // input에 입력된 값 감지, 운동 이름 연관성 비교에 사용될 변수
    let tag_info;   // 기존에 input에서 사용된 비슷한 결과 보여주기용
    let focus_info;     // 엑셀방식에서 사용될 방식, 내용의 길이 표시 용도
    let keydown_info;
    function on_focus(event) {
        tag_info = event.target
    }
    function on_focus_2(event) {
        focus_info = event.target
    }
    function on_keydown(event) {
        keydown_info = event.tartget
    }
    function on_input(event) {
        tag_info = event.target
    }
    function on_blur(event) {   
        // 리스트의 값을 input에 넣어주기 위해 시간지연을 사용했음
        // 또 다른 방법으로는 리스트의 값을 새로운 변수에 저장해주고 이 함수에 
        // tag_info.value = newval; tag_info = undefined; newval = undefined;
        // 이런식으로 해줘도 괜찮을듯
        setTimeout(()=>{tag_info = undefined}, 100)
    } 



/*
<input autocomplete="off"> 를 이용해 자동완성 기능을 끌 수 있음
일단 태그에 직접 입력
*/

    // 태그 생성 감지 테스트
    /*
    let sensor;
    let thisisdiv;
    onMount(()=>{
        const obs = new MutationObserver(ss=>{
            thisisdiv = ss[0].addedNodes[0]
            const sens_del = ss[0].removedNodes
        })
        obs.observe(sensor, {childList:true})
    })
    $: if(thisisdiv) {
        const div_coord = thisisdiv.getBoundingClientRect()
        thisisdiv.style.width = 500+'px'
    }*/

    // 이거 뭐더라?
    function calendar_bool(ccc) {
        cal_bool = []
        for (let i=0; i<ccc.length; i++) {
            let temp_list = []
            for (let j=0; j<7; j++) {
                temp_list.push(false)
            }
            cal_bool.push(temp_list)
        }
    }

    $: calendar_bool(cal)

    // 메뉴상자 컨트롤
    function tool_box_close() {
        event.preventDefault()
        cal_date = undefined
    }
    function tool_box_open(date) {
        event.preventDefault()
        cal_date = date
    }



    function save_program() {
        event.preventDefault()
    }

    // 프로그램 입력 상자 컨트롤
    let program_num_list = [0]
    function remove_input(rm) {
        event.preventDefault()
        const tag_id = 'program' + String(rm)
        const p_div = document.getElementById(tag_id)
        p_div.remove()
    }
    function sub_input() {
        event.preventDefault()
        const formtag = document.getElementById('CP')
        const isitinput = formtag.querySelectorAll('.program_input')
        if (isitinput.length > 1) {
            const num = (event.target.classList[1]).split('_')[2]
            const where = document.getElementById(`program${num}`)
            where.remove()
        }
    }




    // 키보드 방향키 이동
	let k_shift = true
	let k_ctrl = true
	let k_alt = true
    function key_filter(event, key_bool) {      // 동시입력으로 인한 위치 이동 방지, 일단은 shift, ctrl, alt 만
		if (event.key === 'Shift') {k_shift=key_bool}
		if (event.key === 'Control') {k_ctrl=key_bool}
		if (event.key === 'Alt') {k_alt=key_bool}
        if (event.key === 'Tab') {k_shift=true; k_ctrl=true; k_alt=true;}
    }



    let isit_clicked = true; let isit_focus = false; let isit_left = false;
    let WK_list = []    // weight_kind_list, weight칸에 반응하여 weight_kind를 채우기 위해 사용될 변수
    function on_FC(event,i,j,k,bool) { 
        const focus_tag = event.target 
        let length = focus_tag.textContent.length 
        isit_focus = true 
        if (bool) {WK_list=[i,j,k]}
        if(isit_left) {length = 0}
        if(!isit_clicked) {
            const range = document.createRange()
            const selection = window.getSelection()
            range.setStart(focus_tag.firstChild, length)
            range.collapse(true)
            selection.removeAllRanges()
            selection.addRange(range)
        }
    }
    $: if(WK_list.length && WK_list) {

    }
    function on_CL(event) {
        isit_clicked = true 
        isit_left = false
        k_shift = true; k_ctrl = true; k_alt = true;
    }
    function on_KD(event, i, j) {   // keydown
        if (event.key === 'Enter') {
            event.preventDefault()
        }
        isit_clicked = false 
        isit_focus = false
        const tag = event.target
        const tag_class = tag.classList
        const class_length = tag_class.length
        // 날짜, cellnum, cellrow는 클래스 마지막에 위치하도록 만들기
        const cell_date = tag_class[class_length-3]; const cell_num = parseInt(tag_class[class_length-2].split('_')[1]); const cell_row = parseInt(tag_class[class_length-1].split('_')[1])
        let class_index = 0
        //const cell_date = now_num[0]; const cell_num = now_num[1]; const cell_row = now_num[2] 
        const length = event.target.textContent.length 
        const position = window.getSelection().anchorOffset 
        let isit_first = false; let isit_last_cell = false; let isit_last_row = false; // 셀이 처음 또는 마지막인지 판단
        if (num_index[`${cell_date}_last_cell`] === cell_num) {isit_last_cell = true}
        if (num_index[`${cell_date}_last_row`] === cell_row) {isit_last_row = true} 
        if (cell_num === 0) {isit_first = true}
        let lets_move = false       // 이동할지 결정
        let move_class = `${cell_date} `         // 이동할 클래스(마지막 공백 필요함)
 

        if ((event.key === 'ArrowRight' && position === length && !isit_last_cell) || (!isit_last_cell && event.key === 'Enter')) {
            lets_move = true
            move_class = move_class + (`cellnum_${cell_num+1}`)
        } else if (event.key === 'Enter' && isit_last_cell) {
            event.target.blur()
        } else if (event.key === 'ArrowLeft' && position === 0 && !isit_first) {
            lets_move = true
            move_class = move_class + (`cellnum_${cell_num-1}`)
        } else if (event.key === 'ArrowUp' && !isit_first) {
            lets_move = true 
            move_class = move_class + (`cellrow_${cell_row-1}`)
        } else if (event.key === 'ArrowDown' && !isit_last_row) {
            lets_move = true 
            move_class = move_class + (`cellrow_${cell_row+1}`)
        }
        const move_tag = document.getElementsByClassName(move_class)
        if (move_tag[0].id[0]!=='k' && tag.id[0]!=='k' && (event.key==='ArrowUp'||event.key==='ArrowDown')) {
            if (tag.id[0]==='r') {class_index=1}
            else if (tag.id[0]==='w') {class_index=2}
        }
        if (lets_move && k_shift && k_ctrl && k_alt) {
            const range = document.createRange()
            const selection = window.getSelection()
            move_tag[class_index].focus()
            const span_text = move_tag[class_index].childNodes[0]
            let cursor_pos = span_text.length
            if (event.key==='ArrowLeft') {cursor_pos=0}
            range.setStart(span_text, cursor_pos)
            range.collapse(true)
            selection.removeAllRanges()
            selection.addRange(range)
        }
    }
    function weight_kind(event,date,i,j,k,t) {   //  weight_kind 칸 생성
        // weight가 입력되면 weight_kind가 생성됨
        // 만약 테이블에 중량 종류 값이 이미 있으면 api 소통 x
        // 
        const weight_value = event.target.textContent

        let isit_float = true

        if (weight_value) {
            if (weight_value.split('.').length < 3) {
                for(let t of weight_value) {    
                    if(!(parseInt(t) || t==='0' || t==='.')) {isit_float = false; console.log('parse')}
                }
            } else {isit_float = false}
        }
        
        console.log('isit_float', isit_float)
    }
    function WK_change(id, date) {   // 중량 종류 변경에 대한 function
        let wk = event.target.textContent
        if (wk == 'kg') {wk = 'lbs'}
        else {wk = 'kg'}
        update_data(id, 'volume', 'weight_kind', date, wk)
    }
    
    // 우클릭 이벤트 +
    let showcontextmenu = false
    // CM = Context Menu
    let CM_position = [0, 0];   // 마우스 위치를 이용한 CM 생성 위치 지정
    let CM_ex_name = ''; let CM_ex_name_temp = ''   // 종목 이름
    let CM_ex_id = 0
    let CM_date =  ''   // 날짜
    let CM_week = ''
    let add_volume
    let memo_info_temp = {}; let memo_info = {}
    let memo_editor_position_temp = []; let memo_editor_position = []
    let clicked_tag_pos_info = []; let top_tag_pos = []
    let memo_height;    // td 태그의 높이, daily_memo의 높이에 사용될것임
    // program에 대한 contextmenu
    // 우클릭시 변수에 담아야 할 정보 : 운동 이름, 날짜, 메모가 열릴 위치, 
    function program_CM(event) {
        showcontextmenu=false       // 우클릭 메뉴 일단 안보이게
        CM_ex_name_temp = undefined     // 운동 이름 임시(우클릭 메뉴에 사용됨)
        CM_ex_id = undefined
        memo_info_temp = {}     // 데이터 편집에 사용될 리스트인 것 같음
        const tag = event.target 
        const tag_if = ['k_name', 'v_sets', 'v_reps', 'v_kg']
        const top_tag = document.getElementById('top_tag')
        if (tag.closest('td')) {     //  전역변수에 ind 를 저장해서 메모를 update 해야함 //  && tag_if.includes(tag.classList[0])
            event.preventDefault()
            const date = tag.closest('.table_date').classList[1]
            const index = date_to_index(date); const i = index[0]; const j = index[1]
            CM_date = date; CM_week = parseInt(i)+1
            let CTPI_0 = {'right':0, 'top':0}       // clicked_tag_pos_info 리스트의 0번 요소는 exercise_memo를 위한 것 이므로
            if (tag.closest('.program_ex')) {
                const program_ex = tag.closest('.program_ex')
                const tag_id = program_ex.id.split('_')
                CM_ex_id = tag_id[2]; CM_ex_order = tag_id[4]
                CTPI_0 = program_ex.getBoundingClientRect()
                const k = program_ex.classList[1].split('_')[1] // 볼륨칸 추가에 필요한 정보
                add_volume = k
                // 운동 이름 및 데이터 저장에 필요한 인덱스 넘버
                CM_ex_name_temp = program_ex.getElementsByClassName(`k_name p_num${k}`)[0].textContent
                memo_info_temp.k = k
            } else {add_volume = undefined}
            // td 태그의 높이, daily_memo의 높이에 사용될것임
            memo_height = tag.closest('td').clientHeight
            // 메모가 열릴 위치 [exercise_memo, daily_memo]

            clicked_tag_pos_info = [CTPI_0, tag.closest('td').getBoundingClientRect()]
            top_tag_pos = top_tag.getBoundingClientRect()       // top_tag의 좌표
            // 마우스 위치
            const mx = event.clientX; const my = event.clientY;
            CM_position = [mx - top_tag.getBoundingClientRect().x, my - top_tag.getBoundingClientRect().y]
            memo_info_temp.i = i; memo_info_temp.j = j;  
            let temp_temp = [0,1,2,3,4,5,6,7,8,9]
            showcontextmenu = true  // 우클릭 상자 보이게
            } else {showcontextmenu=false}
    }   
    let now_daily_memo;
    let now_exercise_memo;
    $: if(memo_info.length !== 0) {
        let i = memo_info.i; let j = memo_info.j ; let k = memo_info.k
        if(daily_memo[i]) {now_daily_memo = daily_memo[i][j];}
        if(memo[i]) {now_exercise_memo = memo[i][j][k]}   //  memo : line 47 에 있음
    }
    function edit_function(event) { // 우클릭 버튼 클릭 이벤트 설정
        const tag = event.target 
        if (tag.classList[0]==='memo_editor_open') {
            let pos; let fix_x; let fix_y;
            // contextmenu에서 선택된 항목에 따라 생성되는 메모 종류(위치) 지정
            if(tag.classList[1]==='_ex_') {
                pos = clicked_tag_pos_info[0]
                fix_x = 5; fix_y = 0
            } else if (tag.classList[1]==='_da_') {
                pos = clicked_tag_pos_info[1]
                fix_x = 4; fix_y = 0
            }
            memo_editor_position = [pos.right-top_tag_pos.x+fix_x, pos.top-top_tag_pos.y-fix_y]
            memo_info=memo_info_temp;   // [i, j, 운동번호]
            CM_ex_name=CM_ex_name_temp;
        } 
        else if (tag.classList[0]==='volume_add') {create_volume({date:CM_date, exercise_id:CM_ex_id})}
        else if (tag.classList[0]==='volume_sub') {delete_volume({data:CM_data, exercise_order:CM_ex_order})}
        // 주석처리된 부분 수정해야함
    }
    async function volume_add({date, k, bool, SC_id}) { // 볼륨 추가에 대한 update 
        // 기존 프로그램에 끼워넣는 방식
        let control = 'delete_volume'
        if (bool) {control = 'add_volume'}
        await update_program({content:'', date:date, k:k, t:'', memo:'', control:control, btn_action:true})

    }
    let exercise_memo_editor_bool = false
    let daily_memo_editor_bool = false
    function memo_close(event) {
        if (!event.target.closest('._ex_')) {
            exercise_memo_editor_bool=false
        } 
        if (!event.target.closest('._da_')) {
            daily_memo_editor_bool=false
        }
    }
    let LMP_show_i; let LMP_show_j;
    let td_height_list = [] 
    function table_test() {
        td_height_list = []
        const ttt = document.getElementById('table_body')
        const rrr = ttt.querySelectorAll('tr')
        for (let tr of rrr) {
            let temp_height_list = []
            for (let td of tr.querySelectorAll('.program_part')) {
                temp_height_list.push(td.offsetHeight)
            }
            let max_height = Math.max(...temp_height_list)
            td_height_list.push(max_height)
        }
    }
/*
	onMount(()=>{
		const resizeCallback = () => {};
		const resizeObserver = new ResizeObserver(resizeCallback);
		// 감시할 요소
		let targetElement = document.getElementById('table_body');
		// 요소 감시 시작
		resizeObserver.observe(targetElement);
        // 감시할 요소가(요소의 크기가) 변경되면 객체에 들어간 함수형 변수를 실행
	})
    */
/*
    onMount(()=>{
        const callback = (mutationList, observer) => {
            for (const m of mutationList) {
                table_test()
            }
        }
        const observer = new MutationObserver(callback)
        let element = document.getElementById('table_body')
        const config = {childList: true, attribute: true, subtree: true}
        observer.observe(element, config)
    })*/

    function just_test(i, j, date) {
        const ttt = document.getElementById(`${date}/${i}/${j}`)
        const ppp = ttt.querySelectorAll('.program_ex')
        for (const e of ppp) {
            let temp = []
            for (const s of e.querySelectorAll('span')) {
                temp.push(s.textContent)
            }
            temp.push('') 
        }
    }
    // 단축키 판단 리스트
    let SC_key = []
    async function shortcut_key(event, bool) {
        let sck_num = SC_key.length // 계속 눌림 방지
        if (!SC_key.includes(event.key) && bool) {
            SC_key.push(event.key)
        } else if (SC_key.includes(event.key) && !bool) {
            SC_key.splice(SC_key.indexOf(event.key), 1)
        } 

        
        if (SC_key.length && (sck_num !== SC_key.length) && event.target.closest('.program_ex') && event.target.tagName==='SPAN') {
            const now_tag = event.target
            const tag_id = now_tag.id.split('_')
            const exercise_info = now_tag.closest('.program_ex').id.split('_')
            const exercise_date = exercise_info[0]
            const exercise_id = exercise_info[2]
            const exercise_order = exercise_info[4]
            console.log(exercise_info)
            const name = tag_id[0]
            const i = tag_id[2]; const j = tag_id[3]; const k = tag_id[1]; 
            let t;
            if (tag_id.length === 5) {t = tag_id[4]}
              
            
            const tag_class = now_tag.classList
            const date = tag_class[tag_class.length-3]; 
            const cell_num = parseInt(tag_class[tag_class.length-2].split('_')[1])
            const row_num = parseInt(tag_class[tag_class.length-1].split('_')[1])
            if (SC_key.includes('Control') && SC_key.includes('Shift')) {
                if (SC_key.includes('+')) {
                    event.target.blur() // 여기서 event.target의 eventlistener에 의해 on_BL 함수 실행됨
                    await create_volume(exercise_date, exercise_id)
                    document.getElementById(now_tag.id).focus()
                } else if (SC_key.includes('-')) {
                    event.target.blur()
                    await delete_volume(exercise_date, exercise_order)
                    if (document.getElementById(now_tag.id)) {
                        document.getElementById(now_tag.id).focus()
                    } else {
                        document.getElementsByClassName(`${date} cellnum_${cell_num-3}`)[0].focus()
                    }
                }
            }
        }
    }
    // 달력이 완성되었고, focus 하라는 신호와, focus해야할 태그의 정보를 넘겨받으면
    // focus가 실행되는 if문 구현해보기
   
/*
    $: if(volume.length) {
        console.log('volume!')
        console.log(volume)
    }*/
    let cliclicliclic = false
    //$: console.log(ffff)

    // 유사한 운동 이름
    let exercise_similar_list = []
    let similar_list_position = {'x':'', 'y':''}
    let similar_list_show = false   // 리스트 표시 유무
    function make_similat_start(event) {
        let text = event.target.textContent
        let MS_list = my_func.make_similar(text, all_ex)
        console.log(MS_list)
        exercise_similar_list = MS_list[0]
        similar_list_show = MS_list[1]
    }
    function set_list_position(event) {     // 유사 리스트 위치 설정
        let position = event.target.getBoundingClientRect()
        let top_tag = document.getElementById('top_tag').getBoundingClientRect()
        similar_list_position.x = (position.right - top_tag.left) + 5 + 'px'
        similar_list_position.y = (position.top - top_tag.top) + 'px'
    }

// 여기까지 스크립트 입니다.
// ===============================================================================================================================================
// ===============================================================================================================================================
// ===============================================================================================================================================
// ===============================================================================================================================================
// ===============================================================================================================================================
</script>



<svelte:window 
on:contextmenu={()=>{program_CM(event);}}
on:click={()=>{showcontextmenu = false; /*memo_close(event);*/}} 
on:keydown={()=>{shortcut_key(event, true)}}
on:keyup={()=>{shortcut_key(event, false)}}/>


<div id='top_tag'>
    <!-- 운동 목록 검색 유사도 -->
    {#if similar_list_show}
        <div class='similar_list_box' style='left: {similar_list_position.x}; top: {similar_list_position.y};'>
            <ul>
            {#each exercise_similar_list as e}
                <li>{e}</li>
            {/each}
            </ul>
        </div>
    {/if}
    <!-- 우클릭 상자 -->
    {#if showcontextmenu && edit_auth}
        <!-- svelte-ignore a11y-click-events-have-key-events-->
        <!-- svelte-ignore a11y-no-static-element-interactions-->
        <div id='contextmenu_box' style='left: {CM_position[0]}px; top: {CM_position[1]}px;'
        on:click={()=>{edit_function(event)}}>
            <ul>
                <li>삭제</li> <!-- 프로그램 있으면 뜨는거로 바꾸기 -->
                {#if CM_ex_name_temp}
                    <!-- svelte-ignore a11y-click-events-have-key-events-->
                    <!-- svelte-ignore a11y-no-noninteractive-element-interactions-->
                    <li class='memo_editor_open _ex_'
                    on:click={()=>{exercise_memo_editor_bool=true;daily_memo_editor_bool=false;}}>{CM_ex_name_temp} 메모 편집하기</li>
                {/if}
                <!-- svelte-ignore a11y-click-events-have-key-events-->
                <!-- svelte-ignore a11y-no-noninteractive-element-interactions-->
                <li class='memo_editor_open _da_' 
                on:click={()=>{daily_memo_editor_bool=true;exercise_memo_editor_bool=false;}}>{CM_date} 의 메모 편집하기</li>
                <!-- svelte-ignore a11y-click-events-have-key-events-->
                <!-- svelte-ignore a11y-no-noninteractive-element-interactions-->
                <li class='memo_editor_open _we_' on:click={()=>{edit_function(event);}}>{CM_week}주차 메모 편집하기</li>
                <li class='volume_add'>세트x횟수x중량 추가</li>
                <li class='volume_sub'>세트x횟수x중량 제거</li>
            </ul>
        </div>
    {/if}
    <!-- exercise memo -->
    {#if exercise_memo_editor_bool}
        <div class='memo_editor _ex_' style='left: {memo_editor_position[0]}px; top: {memo_editor_position[1]}px;'>
            <p class='memo_editor_title'>{CM_ex_name} 의 메모</p> 
            <a href='/' on:click|preventDefault={()=>{exercise_memo_editor_bool=false}}>x</a>
            <div class='memo_edit_box'>
                <div class='write_memo' contenteditable="true">{now_exercise_memo}</div>

            </div>
        </div>
    {/if}
    <!-- daily memo -->
    {#if daily_memo_editor_bool}
        <div class='memo_editor _da_' style='left: {memo_editor_position[0]}px; top: {memo_editor_position[1]}px;'>
            <p class='memo_editor_title'>{CM_date} 의 메모</p>
            <a href='/' on:click|preventDefault={()=>{daily_memo_editor_bool=false}}>x</a>
            <div class='memo_edit_box'>
                <div class='write_memo' contenteditable="true">{now_daily_memo}</div>
            </div>
        </div>
    {/if}

<!--
    <div bind:this={sensor}>
        <a href='/' on:click={()=>{event.preventDefault(); $year=year_init; $month=month_init;}}>오늘 날짜로 가기</a>
    </div>
    -->
    <!--
    
    <select bind:value={$year}>
        {#each Array.from({length:5}) as _, i}
            <option>{i+2023}</option>
        {/each}
    </select>
    <select bind:value={$month}>
        {#each Array.from({length:12}) as _, i}
            <option>{i+1}</option>
        {/each}
    </select>


    <h1>{$year}.{$month}</h1>
    
    -->

    <table class="main_table"> 
        <thead>
            <tr>
                <!-- weekly memo part -->
                <th>
                    주간 메모
                </th>
                <!-- day part -->
                {#each DD as d}
                    <th>{d}</th>
                {/each}
            </tr>
        </thead>
        <tbody id='table_body'>
        {#if data_ready_2}
        {#each calendar as week, i}
            <!-- weekly memo part -->
            <tr>
                <td class='weekly_memo_box'>
                    <div class='date_part'>
                        <p class='date_part_p'>{params.month}월 {i+1}주차</p>
                    </div>

                    {#if month_weekly_memo[calendar[i][0]]} <!-- 생성시 내용이 중복되는 구조를 피하기 위해 아래와 같이 구성했음 -->
                    <!--svelte-ignore a11y-no-static-element-interactions-->
                    <div class='weekly_memo' spellcheck='false' contenteditable={edit_auth} on:blur={()=>{weekly_memo_BL(calendar[i][0])}}
                        on:keydown={()=>{memo_setting()}}>
                        {@html month_weekly_memo[calendar[i][0]]}
                    </div>  <!-- 백엔드에서 받아온 weekly memo 내용 -->
                    {:else}
                    <!--svelte-ignore a11y-no-static-element-interactions-->
                    <div class='weekly_memo' spellcheck='false' contenteditable={edit_auth} on:blur={()=>{weekly_memo_BL(calendar[i][0])}}
                        on:keydown={()=>{memo_setting()}}>
                    </div> <!-- 저장된 memo가 없을 때 표시할 태그, 또는 새롭게 작성될 메모 -->
                    {/if}
                </td>
            <!-- program part -->
            {#each week as date, j}
                <td class='table_date {date}'> 

                    <!-- date part 날짜가 '오늘' 이라면 색상 다르게 표기-->
                    <div class={(NowMonth===parseInt(date.slice(5,7)) && today===parseInt(date.slice(-2))) ? 'date_part_today' : 'date_part'}>
                        <p class='date_part_p'>{parseInt(date.slice(-2))}</p>
                        <!-- normal mode -->
                        {#if edit_auth}
                        <a href='/' class='add_tool' on:click={()=>(tool_box_open(date))}>설정</a>
                        {/if}
                        {#if cal_date === date}
                            <div 
                            class='add_toolbox' id='toolbox{i}{j}'>
                                <p><a href='/' on:click={()=>{tool_box_close(); delete_program_date(date);}}>삭제</a></p>
                                <p><a href='/' on:click={()=>{tool_box_close()}}>닫기</a></p>
                            </div>
                        {/if}
                    </div>

                    <!-- program part -->
                    <!-- svelte-ignore a11y-no-static-element-interactions-->       <!-- min-height: {td_height_list[i]-4}px; -->
                    <div class='program_part'     
                    on:mouseenter={()=>{LMP_show_i=i; LMP_show_j=j;}}
                    on:mouseleave={()=>{LMP_show_i=undefined; LMP_show_j=undefined;}}>
                        
                            <!-- normal mode -->
                            {#if month_data_2[date]} 
                                <div class='program_ex_example'>
                                    <span class='ex_sets'>sets</span>
                                    <span class='ex_reps'>reps</span>
                                    <span class='ex_kg'>weight</span>
                                </div>
                                {#each month_data_2[date] as ex, k}
                                    <div id='{date}_id_{ex.id}_order_{k}' class='program_ex {date}_{k}'>
                                        <a href='/' class='excel_box_delete edit_btn_{k}' on:click|preventDefault={()=>{delete_box(date, ex, k)}}>x</a>
                                        <a href='/' class='excel_box_add edit_btn_{k}' on:click|preventDefault={()=>{create_box(date, ex, k)}}>+</a>
                                        <span id='k_{k}_{i}_{j}' 
                                        class=
                                        'k_name p_num{k} {date} cellnum_{num_index[`cell_${date}_${k}_n`]} cellrow_{num_index[`row_${date}_${k}_n`]}' 
                                        contenteditable={edit_auth} spellcheck="false"
                                        on:input={()=>{make_similat_start(event);}}
                                        on:focus={()=>{set_list_position(event)}} on:click={()=>{on_CL(event)}}
                                        on:blur={()=>{on_BL(ex.id, 'exercise', 'exercise', date, k, 'n'); similar_list_show=false}}
                                        on:keydown={()=>{on_KD(event, i, j); key_filter(event, false)}} on:keyup={()=>{key_filter(event, true)}}
                                        placeholder='종목 {k}'>
                                            {ex.exercise}
                                        </span>
                                        <div class='volume_box'>
                                            
                                            {#each ex.volumes as vol, t}
                                                <div id='volume_{vol.id}' class='volume_div'>
                                                    <span id='s_{k}_{i}_{j}_{t}' 
                                                    class=
                                                    'v_sets p_num{k} {date} cellnum_{num_index[`cell_${date}_${k}_${t*3}`]} cellrow_{num_index[`row_${date}_${k}_${t}`]}' 
                                                    contenteditable={edit_auth} spellcheck="false"
                                                    on:click={()=>{on_CL(event)}}
                                                    on:blur={()=>{on_BL(vol.id, 'volume', 'set', date, k, t)}}
                                                    on:keydown={()=>{on_KD(event, i, j); key_filter(event, false)}} on:keyup={()=>{key_filter(event, true)}}>{vol.set}</span>
                                                    <span id='r_{k}_{i}_{j}_{t}' 
                                                    class='v_reps p_num{k} {date} cellnum_{num_index[`cell_${date}_${k}_${t*3+1}`]} cellrow_{num_index[`row_${date}_${k}_${t}`]}' 
                                                    contenteditable={edit_auth} spellcheck="false"
                                                    on:click={()=>{on_CL(event)}}
                                                    on:blur={()=>{on_BL(vol.id, 'volume', 'rep', date, k, t)}}
                                                    on:keydown={()=>{on_KD(event, i, j); key_filter(event, false)}} on:keyup={()=>{key_filter(event, true)}}>{vol.rep}</span>
                                                    <p class='v_kg'>
                                                        <span id='w_{k}_{i}_{j}_{t}' 
                                                        class='p_num{k} {date} cellnum_{num_index[`cell_${date}_${k}_${t*3+2}`]} cellrow_{num_index[`row_${date}_${k}_${t}`]}' 
                                                        contenteditable={edit_auth} spellcheck="false"
                                                        on:click={()=>{on_CL(event)}}
                                                        on:blur={()=>{on_BL(vol.id, 'volume', 'weight', date, k, t)}}
                                                        on:keydown={()=>{on_KD(event, i, j); key_filter(event, false);}} on:keyup={()=>{key_filter(event, true)}}
                                                        on:input={()=>{weight_kind(event,date,i,j,k,t);}}>
                                                            {vol.weight}
                                                        </span>
                                                        {#if String(parseFloat(vol.weight))===vol.weight} 
                                                            <span>
                                                                <a id='wk_{k}_{i}_{j}_{t}' class='WK_a' href='/' on:click|preventDefault={()=>{WK_change(vol.id, date)}}>
                                                                    {vol.weight_kind}
                                                                </a>                                            
                                                            </span>
                                                        {/if}
                                                    </p>
                                                </div>
                                            {/each}
                                        </div>  
                                    </div>
                                {/each}
                            {:else}
                                <!-- edit mode short cut -->
                                {#if LMP_show_i===i && LMP_show_j===j && edit_auth}
                                    <!-- svelte-ignore a11y-click-events-have-key-events-->
                                    <div class='lets_make_program' 
                                    on:click={()=>{init_create(event, date)}}>+</div>
                                {/if}
                            {/if}

                    </div>
                </td>
            {/each}
            </tr>
        {/each}
        {/if}
        </tbody>

    </table>
</div>


