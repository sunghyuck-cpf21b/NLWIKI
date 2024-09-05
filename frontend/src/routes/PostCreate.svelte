<script>
    import { link, push } from 'svelte-spa-router'
    import { fastapi, fileapi } from "../lib/api"
    import Error from "../components/Error.svelte"
    import bootstrapMin from 'bootstrap/dist/js/bootstrap.min';
    import Modal from '../lib/Modal.svelte';
    import { onMount } from 'svelte';

    import * as myurl from "../lib/myurl"

    let error = {detail:[]}

    let subject = ''
    //let editcontent = document.getElementById("hereiscontent")
    let content = ''//editcontent.innerText
    //let content_info = ''
    let person = ''
    let occ_date = ''



    function nohome(event) {
        event.preventDefault()
    }

    function post_nonlan(event) {
        if (document.getElementById('content-div-2').innerHTML) {
            content = document.getElementById('content-div-2').innerHTML
            /*const info_ = document.getElementById('content-div-2').childNodes
            let info_list = []
            for (let e of info_) {
                info_list.push(e.nodeType)
            }*/
            //content_info = String(info_list)
        }
        event.preventDefault()
        let url = "/api/nonlan/create"
        let params = {      // 해당 스키마에 입력된 속성들
            subject: subject,
            content: content,
            //content_info: content_info,
            person: person,
            occ_date: occ_date,

        }
        fastapi('post', url, params, 
            (json) => {
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

    let content_box
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
    <h5 class="my-3 border-bottom pb-2">질문 등록</h5>
    <Error error={error} />
    <form method="post" class="my-3">
        <div class="mb-3">
            <label for="subject">제목</label>
            <input id="subject" type="text" class="form-control" bind:value="{subject}">
        </div>
        <div class='mb-3'>
            <label for="person">주요 인물</label>
            <input id="person" type="text" class="form-control" bind:value="{person}">
        </div>
        <div class='mb-3'>
            <label for="occ_date">발생 일시</label>
            <input id="occ_date" type="text" class="form-control" placeholder="2000-01-01 00:00" bind:value="{occ_date}">
        </div>
        <div>
            <a href='/' on:click|preventDefault={()=>{(showModal=true);}}>사진</a>

            <div id='content-div' class='mb-3'>
                <label for='content'>논란 내용</label>
                <div id='content-div-2' class="form-control" style="height: 600px" contenteditable="true" bind:this={content_box}></div>
                <input id='content' style='display: none'>
                <!--<input id="contt" type="text" class="form-control" bind:value="{content}">-->
            </div>
        </div>
           

        <button class="btn btn-primary" on:click='{post_nonlan}'>저장하기</button>
    </form>
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