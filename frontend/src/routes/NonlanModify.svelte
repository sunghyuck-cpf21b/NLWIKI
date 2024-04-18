<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"
    import { is_login } from '../lib/store'

    if(!$is_login) {
        push('/user-login')
    }

    export let params = {}
    const nonlan_id = params.nonlan_id 

    let error = {detail:[]}
    let subject = ''
    let content = ''
    let occ_date = ''
    let person = ''


    function nohome(event) {
        event.preventDefault()
    }

    fastapi("get", "/api/nonlan/detail/"+nonlan_id, {}, (json) => {
        subject = json.subject
        content = json.content
        occ_date = json.occ_date
        person = json.person
    })

    function update_nonlan(event) {
        if (document.getElementById('content-div-2').innerHTML) {
            content = document.getElementById('content-div-2').innerHTML
            /*const info_ = document.getElementById('content-div-2').childNodes
            let info_list = []
            for (let e of info_) {
                info_list.push(e.nodeType)
            }
            content_info = String(info_list)*/
        }
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


    let showModal = false;
    let input;
    let urls = []
    function get_url() {
		const pp = document.getElementById('modal_img')
		for (const f of input.files) {
			const ii = document.createElement('img')
			ii.style.width = '100px'
			ii.style.height = '100px'
			const reader = new FileReader()
			reader.readAsDataURL(f)
			reader.addEventListener('load', function () {
				ii.src = reader.result
				urls = [...urls, reader.result]
				pp.appendChild(ii) 
			})
		}
	}	
	function btn_check() {
        const dd = document.getElementById('content-div-2')
        for (const url of urls) {
            const ii = document.createElement('img')
            ii.src = url
            const img_ratio = 0.5
            ii.style.width = (ii.width*img_ratio)+'px'
            ii.style.height = (ii.height *img_ratio)+'px'
            dd.appendChild(ii)
        }
        showModal = false;
        urls = []
	}
	function btn_cancel() {
		showModal = false;
		urls = []
	}



</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">질문 수정 gggg</h5>
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

        <div>
            <a href='/' on:click={()=>{(showModal=true); nohome(event);}}>사진</a>

            <div id='content-div' class='mb-3'>
                <label for='content'>논란 내용</label>
                <div id='content-div-2' class="form-control" style="height: 600px" contenteditable="true">{@html content}</div>
                <input id='content' style='display: none'>
                <!--<input id="contt" type="text" class="form-control" bind:value="{content}">-->
            </div>
        </div>
        <button class="btn btn-primary" on:click="{update_nonlan}">수정하기</button>
    </form>

</div>

{#if showModal}
<!-- svelte-ignore a11y-no-static-element-interactions -->
<!-- svelte-ignore a11y-click-events-have-key-events -->
    <div class='modal' on:click={()=>(showModal=false)}>
        <div class='modal-content' on:click|stopPropagation>
            <input type='file' bind:this={input} on:change={get_url} multiple accept=".jpg, .jpeg, .png, .gif, .bmp, .webp"/>
            <div id='modal_img' class='modal-content-img'>
            </div>
            <div class='btn-box'>
                <button class='check-btn' on:click={btn_check}>확인</button>
                <button class='cancel-btn' on:click={btn_cancel}>취소</button>
            </div>
        </div>
    </div>
{/if}

<style>
	.modal {
		position: fixed; 
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(0, 0, 0, 0.5);
		display: flex;
		justify-content: center;
    align-items: center;
	}

	.modal-content {
		position: fixed;
		background-color: white;
		width: 600px;
		height: 400px;
    padding: 10px; 
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
	}

	.modal-content-img {
		position: absolute;
		left: 50%;
		top: 20%;
		transform: translate(-50%);
		background-color: gray;
		margin: 0 auto;
		width: 500px;
		height: 200px;
	}

	.btn-box {
		position: absolute;
		left: 50%;
		bottom: 10px;
		transform: translate(-50%);
		background-color: white; 
		width: 200px;
		margin: 0 auto;
		text-align: center
	}
	
	.check-btn {
		width: 70px;
		margin: 0 10px;
	}

	.cancel-btn {
		width: 70px;
		margin: 0 10px;
	}

    #content-div-2 {
        overflow: auto;
    }
  </style>