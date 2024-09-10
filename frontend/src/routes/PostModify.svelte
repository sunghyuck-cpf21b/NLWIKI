<script>
    import { push } from 'svelte-spa-router'
    import {fastapi} from "../lib/api"
    import Error from "../components/Error.svelte"
    import { is_login } from '../lib/store'

    import * as api_funcs from '../lib/api_funcs'
    import * as myurl from "../lib/myurl"

    if(!$is_login) {
        push(myurl.userlogin_url)
    }

    export let params = {}
    const post_id = params.post_id 

    let error = {detail:[]}
    let subject = ''
    let content = ''
    let occ_date = ''
    let person = ''


    function nohome(event) {
        event.preventDefault()
    }

    let categories = []
    let selected_category
    api_funcs.get_categories({task:'create'}).then(data=>{
        categories = data
    })

    fastapi("get", "/api/post/detail/"+post_id, {}, (json) => {
        selected_category = json.category
        subject = json.subject
        content = json.content
        occ_date = json.occ_date
        person = json.person
    })

    function update_post(event) {
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
        let url = "/api/post/update"
        let params = {
            post_id: post_id,
            subject: subject,
            content: content,
            occ_date, occ_date,
            person: person,
        }
        fastapi('put', url, params,
            (json) => {
                push(myurl.postdetail_url+post_id)
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

    <Error error={error} />
    <div class="input_box">
        <select class='select_category' on:change={()=>{selected_category=event.target.value}} bind:value={selected_category}>
            {#each categories as c}
            <option style={(c=='논란') ? 'color: #ff0000':''}>{c}</option>
            {/each}
        </select>
        <div class="subject_box">
            <label for="subject"></label>
            <input id="subject" type="text" placeholder="제목을 입력해주세요" class="form-control" bind:value="{subject}">
        </div>
        {#if selected_category == '논란'}
        <div class='person_box'>
            <label for="person"></label>
            <input id="person" type="text" placeholder="주요 인물을 입력해주세요" class="form-control" bind:value="{person}">
        </div>
        <div class='occ_data_box'>
            <label for="occ_date">select로 변경하기</label>
            <input id="occ_date" type="text" class="form-control" placeholder="2000-01-01 00:00" bind:value="{occ_date}">
        </div>
        {/if}
        <div>
            <a href='/' on:click|preventDefault={()=>{(showModal=true);}}>사진</a>

            <div id='content-div' class='mb-3'>
                <label for='content'>내용</label>
                <div id='content-div-2' class="form-control" style="height: 600px" contenteditable="true">{@html content}</div>
                <input id='content' style='display: none'>
                <!--<input id="contt" type="text" class="form-control" bind:value="{content}">-->
            </div>
        </div>
           

        <button class="btn btn-primary" on:click='{update_post}'>저장하기</button>
    </div>
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