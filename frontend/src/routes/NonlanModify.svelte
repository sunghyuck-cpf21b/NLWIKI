<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"

    export let params = {}
    const nonlan_id = params.nonlan_id 

    let error = {detail:[]}
    let subject = ''
    let content = ''
    let occ_date = ''
    let person = ''

    fastapi("get", "/api/nonlan/detail/"+nonlan_id, {}, (json) => {
        subject = json.subject
        content = json.content
        occ_date = json.occ_date
        person = json.person
    })

    function update_nonlan(event) {
        event.preventDefault()
        let url = "/api/nonlan/update"
        let params = {
            nonlan_id: nonlan_id,
            subject: subject,
            content: content,
            occ_date, occ_date,
            person: person,
        }
        fastapi('put', url, params,
            (json) => {
                push('/detail/'+nonlan_id)
            },
            (json_error) => {
                error = json_error
            })
    }

</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">질문 수정</h5>
    <Error error={error} />
    <form method="post" class="my-3">
        <div class="mb-3">
            <label for="subject">제목</label>
            <input type="text" class="form-control" bind:value="{subject}">
        </div>
        <div class="mb-3">
            <label for="person">주요 인물</label>
            <input type="text" class="form-control" bind:value="{person}">
        </div>
        <div class="mb-3">
            <label for="occ_date">발생 일시</label>
            <input type="text" class="form-control" placeholder="2000-00-00 00:00" bind:value="{occ_date}">
        </div>

        <div class="mb-3">
            <label for="content">내용</label>
            <textarea class="form-control" rows="10" bind:value="{content}"></textarea>
        </div>
        <button class="btn btn-primary" on:click="{update_nonlan}">수정하기</button>
    </form>

</div>