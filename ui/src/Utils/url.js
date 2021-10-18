export const getServer = () => process.env.REACT_APP_API_URL;

export const minimizeAddress = (address) => {
  return (
    address.substr(0, 8) +
    '.....' +
    address.substr(address.length - 8, address.length)
  );
};
export const getBase64 = (file) => {
  return new Promise((resolve) => {
    let baseURL = '';
    // Make new FileReader
    let reader = new FileReader();

    reader.readAsDataURL(file);

    reader.onload = () => {
      baseURL = reader.result;
      resolve(baseURL);
    };
  });
};
