function recallQUery(queries) {
  let queryString = '',
    i = 0;
  for (let query of queries) {
    if (i !== 0) {
      queryString += ',';
    }
    switch (query.operator) {
      case '$like':
        switch (query.type) {
          case 'n%':
            queryString +=
              query.value !== ''
                ? `${query.field}: {_like: "${query.value}%"}`
                : '';
            break;
          case '%n%':
            queryString +=
              query.value !== ''
                ? `${query.field}: {_like: "%${query.value}%"}`
                : '';
            break;
          default:
            queryString +=
              query.value !== ''
                ? `${query.field}: {_like: "%${query.value}"}`
                : '';
        }
        break;
      case '$eq':
        queryString +=
          query.value !== '' ? `${query.field}: {_eq: "${query.value}"}` : '';
        break;
      case '$subquery':
        queryString +=
          query.value !== ''
            ? `${query.field}: {${recallQUery(query.queries)}}`
            : '';
        break;
      default:
        queryString += '';
    }
    i++;
  }
  return queryString;
}

export default function parse(querys = []) {
  let queryString = '',
    i = 0;
  for (let query of querys) {
    if (i !== 0) {
      queryString += ',';
    }
    switch (query.operator) {
      case '$like':
        switch (query.type) {
          case 'n%':
            queryString +=
              query.value !== ''
                ? `${query.field}: {_like: "${query.value}%"}`
                : '';
            break;
          case '%n%':
            queryString +=
              query.value !== ''
                ? `${query.field}: {_like: "%${query.value}%"}`
                : '';
            break;
          default:
            queryString +=
              query.value !== ''
                ? `${query.field}: {_like: "%${query.value}"}`
                : '';
        }
        break;
      case '$eq':
        queryString +=
          query.value !== '' ? `${query.field}: {_eq: "${query.value}"}` : '';
        break;
      case '$subquery':
        queryString +=
          query.value !== ''
            ? `${query.field}: {${recallQUery(query.queries)}}`
            : '';
        break;
      default:
        queryString += '';
    }
    i++;
  }
  return `where:{${queryString}}`;
}
