<script>
    import { push } from 'svelte-spa-router'
    import { fastapi, fileapi } from "../lib/api"
    import Error from "../components/Error.svelte"
    import { is_login } from '../lib/store'
    import { onMount } from 'svelte';

    import * as store from '../lib/store'
    import * as api_funcs from '../lib/api_funcs'
    import * as myurl from "../lib/myurl"

    import moment from 'moment'
    moment.locale('ko')

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

    let occ_date_list = []
    fastapi("get", "/api/post/detail/"+post_id, {}, (json) => {
        selected_category = json.category
        subject = json.subject
        content = json.content
        occ_date = moment(json.occ_date).format('YYYY-MM-DD')
        occ_date_list = occ_date.split('-')
        person = json.person
    })
    
    $: selected_year = parseInt(occ_date_list[0])
    $: selected_month = parseInt(occ_date_list[1])
    $: selected_date = parseInt(occ_date_list[2])
    $: last_date = new Date(selected_year, selected_month, 0).getDate()

    function add_0(num) {
        if (num < 10) {
            return '0'+num
        }
        else {
            return num
        }
    }

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
        let _occ_date 
        if (selected_category === '논란') {
            let date = add_0(selected_month)
            let month = add_0(selected_month)
            let _occ_date = `${selected_year}-${month}-${date}`
        }
        
        let url = "/api/post/update"
        let params = {
            post_id: post_id,
            category: selected_category,
            subject: subject,
            content: content,
            occ_date: _occ_date,
            person: person,
        }
        console.log(params)
        fastapi('put', url, params,
            (json) => {
                store.now_page.set(1)
                push(myurl.postdetail_url+'/'+post_id)
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
            if (i.size/(1024*1024) < 10) {
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
        if (temp_alert) {alert_function('이미지 크기는 10MB보다 작아야 합니다.')}
        showModal = false;
    }

    async function copy_img_post(data) {
        const padding = (data.match(/=/g) || []).length 
        const b64length = data.length*0.75 - padding 
        if (b64length/(1024*1024) > 10) {
            alert_function('이미지 크기는 10MB보다 작아야 합니다.')
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
                >{@html content}</div>
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