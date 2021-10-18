export const getServer = () => process.env.REACT_APP_API_URL;

export const minimizeAddress = (address) => {
  return (
    address.substr(0, 8) +
    '.....' +
    address.substr(address.length - 8, address.length)
  );
};
