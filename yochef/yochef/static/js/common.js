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
    fetch(url, {
        method: method,
        body: formData,
        headers: { "X-CSRFToken": parse_cookies().csrftoken },
    }).then(response => response.json())
    .then(response => callBackFunc(response))
    .catch(error => console.error('Error: ',error))
}

// 지역을 가져오는 함수입니다
function getRegion(region = 1){sendAjax('GET', '/getRegion/'+region, setRegion);}

function setRegion(data){
    let options = '';
    let region = data["region"];
    delete data["region"];
    for (let id in data) {
        if (id == region){
            options += `<option value="${id}" selected>${data[id]}</option>`;
        } else{
            options += `<option value="${id}">${data[id]}</option>`;
        }
    }
    document.getElementsByName('residence')[0].innerHTML = options;
}

// 세부 지역을 가져오는 함수입니다.
function getRegionDetail(regionId, regionDetailId = 0){
    let formData =  new FormData();
    formData.append('region_id', regionId);
    formData.append('region_detail_id', regionDetailId);
    sendAjax('POST', '/getRegionDetail', setRegionDetail, formData);
}

function setRegionDetail(data){
    regionDetailId = data.region_detail_id
    data = data.region_details;
    let options = ``;
    let resDetail = document.getElementsByName('residenceDetail')[0];
    for (resid of data) options += `<option value="${resid.id}">${resid.detailName}</option>`;
    resDetail.classList.replace("hide", "show");
    resDetail.innerHTML = options;
    selectedRegion = document.querySelector(`select[name="residenceDetail"] > option[value="${regionDetailId}"]`)

    if (selectedRegion){
        selectedRegion.setAttribute('selected',"")
    }
}
