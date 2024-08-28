import { findBestMatch } from 'string-similarity';
import { access_token, username, is_login } from './store';

// 유사한 운동 이름
export function make_similar(text, all_ex) {      // 유사 리스트 생성 함수
    let exercise_similar_list = []
    // 한글 특성상 완성되지 않은 글자가 있기 때문에 마지막 글자를 제거한 text_1 도 같이 사용

    let text_1;
    if (text.length > 1) {text_1 = text.slice(0, text.length-1)}    // 입력된 문자열 길이가 2개 이상일 때 text_1 생ㅇ성
    // 전체 운동 이름 중 가장 유사한 순서대로 10개만 추리기
    let test = findBestMatch(text, all_ex).ratings.sort((a, b)=> b.rating - a.rating)  
    let temp = []   // 유사한 이름 리스트
    for (let i=0; i<10; i++) {  // 유사도가 0보다 높은거만 10개
        if (test[i].rating > 0) {temp.push(test[i].target)} 
        else if (test[i].rating == 0) {break} // 더 이상 0보다 큰 유사도가 없다면 반복문 종료
    }
    let temp_start = [] // 해당 문자열로 시작
    let temp_start_1 = []   // 해당 문자열[0:-1] 로 시작
    if (text.length) {
        for (const e of all_ex) {
            if (e.startsWith(text)) {temp_start.push(e)} 
            else if (e.startsWith(text_1)) {temp_start_1.push(e)}
        }
    }
    // 중요도에 따라 최종 리스트를 15개로 정리 
    exercise_similar_list = [...new Set([...temp_start, ...temp, ...temp_start_1])]
    exercise_similar_list = exercise_similar_list.slice(0, 15)
    let similar_list_show = Boolean(text.length) && Boolean(exercise_similar_list.length) // 유사도 표시 준비 판단
    // 중요도 : temp_start > temp > temp_start_1
    // 시작 문자열 > 유사 문자열 > 문자열[:-1]로 시작
    return [exercise_similar_list, similar_list_show]
}

export function logout() {
    access_token.set('')
    username.set('')
    is_login.set(false)
}