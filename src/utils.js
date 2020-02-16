export const saveJson = (data, fname) => {
  data = encodeURIComponent(JSON.stringify(data));
  data = `data:text/json;charset=utf-8,${data}`;
  let link = document.createElement('a');
  link.setAttribute('href', data);
  link.setAttribute('download', fname);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};
