<script>
    import { link, push } from 'svelte-spa-router'
    import { fastapi, fileapi } from "../lib/api"
    import Error from "../components/Error.svelte"
    import bootstrapMin from 'bootstrap/dist/js/bootstrap.min';
    import Modal from '../lib/Modal.svelte';
    import { onMount } from 'svelte';
    import * as store from "../lib/store"

    import * as api_funcs from '../lib/api_funcs'
    import * as myurl from "../lib/myurl"

    let selected_year = store.ST_year
    let selected_month = store.ST_month
    let selected_date = store.ST_date
    $: last_date = new Date(selected_year, selected_month, 0).getDate()


    let error = {detail:[]}

    let subject
    //let editcontent = document.getElementById("hereiscontent")
    let content//editcontent.innerText
    //let content_info = ''
    let person

    function nohome(event) {
        event.preventDefault()
    }

    let categories = []
    let selected_category = '일반'
    api_funcs.get_categories({task:'create'}).then(data=>{
        categories = data
    })

    function add_0(num) {
        if (num < 10) {
            return '0'+num
        }
        else {
            return num
        }
    }

    function post_post(event) {
        if (document.getElementById('content-div-2').innerHTML) {
            content = document.getElementById('content-div-2').innerHTML
            /*const info_ = document.getElementById('content-div-2').childNodes
            let info_list = []
            for (let e of info_) {
                info_list.push(e.nodeType)
            }*/
            //content_info = String(info_list)
        }
        let occ_date 
        if (selected_category === '논란') {
            let date = add_0(selected_month)
            let month = add_0(selected_month)
            let occ_date = `${selected_year}-${month}-${date}`
        }
        console.log(occ_date)
        event.preventDefault()
        let url = "/api/post/create"
        let params = {      // 해당 스키마에 입력된 속성들
            category: selected_category,
            subject: subject,
            content: content,
            //content_info: content_info,
            person: person,
            occ_date: occ_date,
        }
        console.log(params)
        fastapi('post', url, params, 
            (json) => {
                store.now_page.set(1)
                push(myurl.postlist_url)
            },
            (json_error) => {
                error = json_error
            }
        )

    }

    function img_pop(event) {
        event.preventDefault()
        window.open('upload/image', '_blank', 'width=600.height=400')
    }

/*
    function post_image(event) {
        event.preventDefault()
        let url = "/api/image/upload"
        let params = {
            file: file,
        }
        fastapi('post', url, params,
            (json) => {
                // 응답이 성공적이면 이미지 미리보기를 띄우기?
            })
    }
*/



    // Modal
    let showModal = false;
    let input;
    //let urls_total = []
    let urls = []
    function onModal() {
        showModal = true
    }
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
        // 함수 수정하기
        // 확인 버튼을 누르면 이미지를 전송 
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

    function file_send() {

    }

    function imgtag_maker({CD, src_url, width, height}) {
        console.log(src_url, width, height)
        const ii = document.createElement('img')
        ii.src = src_url 
        if (width > 600) {
            height = height * (600 / width)
            ii.style.width = 600 + 'px'
            ii.style.height = height  + 'px'
        }
        CD.appendChild(ii)
    }

    async function testtt() {
        const url = '/api/file/img'
        const dd = document.getElementById('content-div-2')
        for (const i of input.files) {
            const fd = new FormData()
            fd.append('file', i)
            const params = fd
            console.log('api 호출 직전')
            await fileapi(url, params, 
                async (json)=>{
                    await imgtag_maker({CD: dd, src_url: json.image_url, width: json.width, height: json.height})
                }
        )
        }
        showModal = false;
    }
</script>





<div class="container">

    <Error error={error} />
    <div class="input_box">
        <select class='select_category' on:change={()=>{selected_category=event.target.value}}>
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
            <label for="occ_date"></label>
            <select bind:value={selected_year}>
                {#each Array.from({length:10}) as _, i}
                <option>{store.ST_year-i}</option>
                {/each}
            </select>
            <select bind:value={selected_month}>
                {#each Array.from({length:12}) as _, i}
                <option>{1+i}</option>
                {/each}
            </select>
            <select bind:value={selected_date}>
                {#each Array.from({length:parseInt(last_date)}) as _, i}
                <option>{1+i}</option>
                {/each}
            </select>
        </div>
        {/if}
        <div>
            <a href='/' on:click|preventDefault={()=>{(showModal=true);}}>사진</a>

            <div id='content-div' class='mb-3'>
                <label for='content'>내용</label>
                <div id='content-div-2' class="form-control" style="height: 600px" contenteditable="true"></div>
                <input id='content' style='display: none'>
                <!--<input id="contt" type="text" class="form-control" bind:value="{content}">-->
            </div>
        </div>
           

        <button class="btn btn-primary" on:click='{post_post}'>저장하기</button>
    </div>
</div>



{#if showModal}
<!-- svelte-ignore a11y-no-static-element-interactions -->
<!-- svelte-ignore a11y-click-events-have-key-events -->
    <div class='modal' on:click={()=>(showModal=false)}>
        <div class='modal-content' on:click|stopPropagation>
            <input type='file' bind:this={input} on:change={()=>{get_url();}} multiple accept=".jpg, .jpeg, .png, .gif, .bmp, .webp"/>
            <div id='modal_img' class='modal-content-img'>
            </div>
            <div class='btn-box'>
                <button class='check-btn' on:click={()=>{testtt();}}>확인</button>
                <button class='cancel-btn' on:click={btn_cancel}>취소</button>
            </div>
        </div>
    </div>
{/if}





<!--
<Modal bind:showModal>
    <h2 slot='header'>
        사진
    </h2> 
    <input type='file' multiple bind:this={inputIMG} on:change={get_url}  accept=".jpg, .jpeg, .png, .gif, .bmp, .webp"/>
    <div id='subun_img' style='height:200px'>
        
    </div>
    <button>확인</button>
</Modal>
-->

<!--
    script에서 작성한 함수를 사용하려면
    '{func}'
    방식으로 사용하기
-->

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