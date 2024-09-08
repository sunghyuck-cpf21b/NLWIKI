<script>
    import {fastapi} from "../lib/api";

    let personal_memo
    async function get_p_memo() {
        const url = '/api/'
    }
</script>


<div class='sidebar'>
    <img src="https://i.namu.wiki/i/7nt7Vamtf_Z7ak4-ZqA7f87AL8WKNW15g-G_ZsU_ytigl9QPSKnJbZD82ikRYGC6RSjVPCyhqKa5gq9YwQwu8Osk9l46ixY8cNmgEZNIRf5NvSAK8bCHA189RA2lRC0XivujQdXCJtSZJene17zvcQ.webp" 
    alt='' style='width: 100%;'>
    <div class='personal_memo' contenteditable="true">

    </div>
</div>

<style>
    .sidebar {
        border: 1px solid;
        height: 500px;
        overflow: scroll;
    }
    .personal_memo {
        width: 100%;
        min-height: 100%;
    }
</style>