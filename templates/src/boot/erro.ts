import { boot } from 'quasar/wrappers';
import {AxiosError} from 'axios';
import {Notify} from 'quasar';

export default boot(({ Vue }) => {
  // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
  Vue.prototype.$erro = function (error:AxiosError) {
    console.log(error);
    console.log(error.response);
    if (error.response === undefined) {
      if (error.stack) {
        Notify.create({
          type: 'negative',
          caption: 'Ocorreu um erro ao processar sua solicitação.',
          message: error.message + error.stack,
          multiLine: true
        });
      } else {
        Notify.create({
          type: 'negative',
          caption: 'Ocorreu um erro ao processar sua solicitação.',
          message: String(error)
        });
      }
    }
  };
});