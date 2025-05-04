//输出的内容粘贴到input.txt
const MEDIA_ID = 1111111111;  //改成需要复制的id

async function exportAll() {
    let all = [];
    let page = 1;
    while (true) {
        const res = await fetch(`https://api.bilibili.com/x/v3/fav/resource/list?media_id=${MEDIA_ID}&pn=${page}&ps=20`);
        const data = await res.json();
        if (!data.data.medias) break;
        all = all.concat(data.data.medias);
        console.log(`已加载第${page}页，累计${all.length}条`);
        if (data.data.has_more) page++;
        else break;
        await new Promise(r => setTimeout(r, 1000));
    }
    return all;
}

exportAll().then(data => console.log(data));