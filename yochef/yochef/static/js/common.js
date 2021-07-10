// 기본으로 세팅된 함수입니다. 삭제하지 말아주세요!
function parse_cookies() {
    var cookies = {};
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(function (c) {
            var m = c.trim().match(/(\w+)=(.*)/);
            if(m !== undefined) {
                cookies[m[1]] = decodeURIComponent(m[2]);
            }
        });
    }
    return cookies;
}

function sendAjax(method, url, callBackFunc=()=>{}, formData=null){
    let xml = new XMLHttpRequest()
    xml.onreadystatechange = (()=>{
        if (xml.readyState == 4 && xml.status ==200){
            callBackFunc(JSON.parse(xml.responseText));
        }
    });
    let cookies = parse_cookies();
    xml.open(method, url);
    xml.setRequestHeader('X-CSRFToken', cookies.csrftoken);
    xml.send(formData);
}

// 지역을 가져오는 함수입니다
function getRegion(){sendAjax('GET', '/getRegion', setRegion);}

function setRegion(data){
    let options = '';
    for (let id in data) options += `<option value="${id}">${data[id]}</option>`;
    document.getElementsByName('residence')[0].innerHTML = options;
}

// 세부 지역을 가져오는 함수입니다.
function getRegionDetail(regionId){
    let formData =  new FormData()
    formData.append('region_id', regionId)
    sendAjax('POST', '/getRegionDetail', setRegionDetail, formData);
}

function setRegionDetail(data){
    data = data.region_details;
    let options = ``;
    let resDetail = document.getElementsByName('residenceDetail')[0];
    for (resid of data) options += `<option value="${resid.id}">${resid.detailName}</option>`;
    resDetail.classList.replace("hide", "show");
    resDetail.innerHTML = options;
}