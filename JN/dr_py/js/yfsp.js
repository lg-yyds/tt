var rule = {
    title: '爱一帆',
    host: 'https://www.yfsp.tv',
    url: '/list/fyclass?page=fypage',
    searchUrl: '',
    searchable: 0,
    quickSearch: 0,
    filterable: 0,
    headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
        'Referer': 'https://www.yfsp.tv/'
    },
    timeout: 8000,
    class_name: '电影&剧集&动漫&记录片&综艺',
    class_url: 'movie&drama&anime&documentary&variety',
    // 推荐/首页
    推荐: '*',
    // 一级列表（对应 yfsp.json 的 vod_*）
    一级: `js:
        pdfh = jsp.pdfh; pdfa = jsp.pdfa; pd = jsp.pd;
        let d = [];
        let html = request(input);
        let list = pdfa(html, "ul.video_list li") || pdfa(html, ".video_list li") || [];
        list.forEach(it => {
            let title = pdfh(it, "h3&&Text") || pdfh(it, "h3 a&&Text") || "";
            let img = pd(it, "img&&data-src") || pd(it, "img&&src") || "";
            let link = pd(it, "a&&href") || "";
            let score = pdfh(it, "div.score&&Text") || pdfh(it, ".score&&Text") || "";
            if (title && link) {
                d.push({
                    title: title.trim(),
                    img: img,
                    desc: score,
                    url: link
                });
            }
        });
        setResult(d);
    `,
    // 二级详情 + 选集（playlist_flag=false，但保留 playlist 选择器兜底）
    二级: `js:
        pdfh = jsp.pdfh; pdfa = jsp.pdfa; pd = jsp.pd;
        VOD = {};
        let html = request(input);
        VOD.vod_name = pdfh(html, "h1&&Text") || pdfh(html, "h2&&Text") || pdfh(html, "title&&Text").split("-")[0].trim() || "";
        VOD.vod_pic = pd(html, "img&&data-src") || pd(html, "img&&src") || pd(html, "meta[property=og:image]&&content") || "";
        VOD.vod_content = pdfh(html, "div.summary&&Text") || pdfh(html, ".summary&&Text") || pdfh(html, "meta[name=description]&&content") || "";
        VOD.vod_remarks = "";
        let tabs = [];
        let lists = [];
        // 原 json: playlist_group_node = //div[@class='n-media-list']//a
        let eps = pdfa(html, "div.n-media-list a") || pdfa(html, ".n-media-list a") || pdfa(html, "[class*=n-media-list] a") || [];
        if (eps.length === 0) {
            eps = pdfa(html, ".playlist a") || pdfa(html, ".play-list a") || pdfa(html, "[class*=playlist] a") || [];
        }
        if (eps.length > 0) {
            let urls = [];
            eps.forEach(a => {
                let ep = pdfh(a, "a&&Text") || pdfh(a, "Text") || ("第" + (urls.length + 1) + "集");
                let href = pd(a, "a&&href") || pd(a, "href");
                if (href) urls.push(ep.trim() + "$" + href);
            });
            if (urls.length) {
                tabs.push("默认");
                lists.push(urls.join("#"));
            }
        }
        // 无选集时：详情页本身作为播放入口（对应 open_with_safari）
        if (lists.length === 0) {
            tabs.push("默认");
            lists.push("播放$" + input);
        }
        VOD.vod_play_from = tabs.join("$$$") || "默认";
        VOD.vod_play_url = lists.join("$$$");
    `,
    // 原 json search_flag=false，关闭搜索
    搜索: '',
    // 播放：优先抽直链，否则返回页面嗅探
    lazy: `js:
        if (!/^http/.test(input)) {
            input = rule.host + (input.startsWith("/") ? input : "/" + input);
        }
        try {
            let html = request(input, {headers: rule.headers});
            let m = html.match(/player_aaaa\\s*=\\s*(\\{[\\s\\S]*?\\})/) || html.match(/var\\s+player_.*?=\\s*(\\{[\\s\\S]*?\\})/);
            if (m) {
                try {
                    let conf = JSON.parse(m[1]);
                    let u = conf.url || conf.uri || "";
                    if (u) {
                        if (!/^http/.test(u) && conf.encrypt) {
                            input = { parse: 1, jx: 1, url: u };
                        } else {
                            if (!/^http/.test(u)) u = rule.host + (u.startsWith("/") ? u : "/" + u);
                            input = { parse: 0, jx: 0, url: u, header: rule.headers };
                        }
                    }
                } catch (e) {}
            }
            if (typeof input === "string" || (input && input.parse === undefined && !input.url)) {
                let m3u8 = html.match(/https?:\\/\\/[^"'\\s]+\\.m3u8[^"'\\s]*/i);
                let mp4 = html.match(/https?:\\/\\/[^"'\\s]+\\.mp4[^"'\\s]*/i);
                if (m3u8) {
                    input = { parse: 0, jx: 0, url: m3u8[0], header: rule.headers };
                } else if (mp4) {
                    input = { parse: 0, jx: 0, url: mp4[0], header: rule.headers };
                } else {
                    input = { parse: 1, jx: 0, url: input, header: rule.headers };
                }
            }
        } catch (e) {
            input = { parse: 1, jx: 0, url: input };
        }
    `,
    play_parse: true,
    图片来源: '',
    图片替换: '',
    预处理: '',
    double: false,
    tab_exclude: '猜你|喜欢|下载|剧情|榜|评论',
    cate_exclude: '首页|留言|APP|下载|资讯|新闻|动态'
};