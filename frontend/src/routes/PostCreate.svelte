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
            console.log(selected_category)
            let date = add_0(selected_month)
            let month = add_0(selected_month)
            occ_date = `${selected_year}-${month}-${date}`
        }
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
    let input; // 이미지 파일 입력되는 변수

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
            console.log(reader.files)
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

    let alert_message = ''
    let showAlert = false
    function alert_function(message) {
        alert_message = message 
        showAlert = true 
        setTimeout(()=>{
            showAlert = false
        }, 4000)
    }


    async function testtt() { // 이미지 백엔드 서버에 저장하고 url 가져오는 함수
        const url = '/api/file/img'
        const dd = document.getElementById('content-div-2')

        let temp_alert = false
        for (const i of input.files) {
            if (i.size/(1024*1024) < 5) {
                const fd = new FormData()
                fd.append('file', i)
                const params = fd
                console.log('api 호출 직전')
                await fileapi(url, params, 
                    async (json)=>{
                        await imgtag_maker({CD: dd, src_url: json.image_url, width: json.width, height: json.height})
                    }     
                )
            } else {
                temp_alert = true
            } 
        }
        if (temp_alert) {alert_function('이미지 크기는 5MB보다 작아야 합니다.')}
        showModal = false;
    }

    async function copy_img_post(data) { // 복붙한 이미지 데이터를 백엔드로 전송하고 url을 반환하는 함수
        // base64 형태 그대로 전달
        // 단, base64 문자열 데이터는 기존 데이터의 1.33배 라고 함
        // 추후에 파일로 변환해서 전송하는 방법으로 변경하기

        // 전송 전에 파일 용량 확인
        const padding = (data.match(/=/g) || []).length 
        const b64length = data.length*0.75 - padding 
        if (b64length/(1024*1024) > 5) {
            alert_function('이미지 크기는 5MB보다 작아야 합니다.')
            return 
        } else {
            const url = '/api/file/b64_img'
            const params = {
                data: data,
            }
            let result = {}
            await fastapi('post', url, params, 
                (json)=>{
                    result = json
                }
            )
            return result
        }
    }

    let content_div
    onMount(()=>{ // 내용 입력칸에 복붙한 이미지를 감지하기 위한 코드
        const observer = new MutationObserver((muts)=>{
            muts.forEach((mut)=>{
                mut.addedNodes.forEach(node=>{
                    if (node.nodeName === 'IMG') {
                        copy_img_post(node.src).then(data=>{ // 이미지 데이터와 교환한 url을 받아 src 내용을 변경 및 사이즈 조정
                            node.src = data.image_url
                            if (data.width > 600) {
                                height = data.height * (600/data.width)
                                node.style.width = data.width + 'px'
                                node.style.height = height + 'px'
                            }
                        })
                    }
                })
            })
        })
        observer.observe(content_div, {
            childList: true,
            subtree: true,
        })
    })

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
                <div id='content-div-2' class="form-control" style="height: 600px" contenteditable="true"
                bind:this={content_div}
                ></div>
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

{#if showAlert}
<div class='alert_st'>
    <span>
        {alert_message}
    </span>
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
		text-align: center;
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

    .alert_st {
        height: 100px;
        background-color: var(--bs-danger-bg-subtle);
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        border: 1px solid var(--bs-danger-border-subtle);
        border-radius: var(--bs-border-radius);
        
        display: flex;
        align-items: center;
        justify-content: center;

        font-weight: bolder;
        color: var(--bs-danger-text-emphasis);

        padding: 10px;
    }
  </style>