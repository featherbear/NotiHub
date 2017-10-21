const Netbank = require('node-cba-netbank');

const netbank = new Netbank();

netbank.logon('', '')
  .then(resp => {
    //  output account to console
    resp.accounts.forEach(
      a => console.log(`${a.name} (${a.bsb} ${a.account}) => ${a.balance}/${a.available}`)
    );

  })
  .catch(console.error);
