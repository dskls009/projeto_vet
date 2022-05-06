<template>
  <q-layout
    view="hHh lpR fFf"
    style="background-color: #1976D2;"
  >
    <q-page-container
      class="full-width row wrap justify-center items-center content-center fixed-full"
      :style="'background-size: cover;background-image: url(' + params.backimg + ')'"
    >
      <q-form
        @submit="onSubmit"
        class="q-gutter-md"
        @keyup.enter="onSubmit"
      >
        <q-card class="login-card">
          <div
            class="bg-white text-h3 text-white text-center"
            style="position: static;vertical-align:middle;padding: 10px;"
          >
          </div>
          <q-card-section>
            <div class="text-h6">Login</div>
          </q-card-section>
          <q-card-section class="q-pt-none">
            <q-input
              filled
              v-model="params.form.username"
              label="Usuário"
              lazy-rules
              autofocus
              square
              :rules="[ val => val && val.length > 0 || 'Campo Obrigatório!']"
            />
            <q-input
              filled
              square
              type="password"
              v-model="params.form.password"
              label="Senha"
              lazy-rules
              :rules="[
          val => val !== null && val !== '' || 'Campo Obrigatório!'
        ]"
            />
          </q-card-section>
          <q-separator/>
          <q-card-actions align="around">
            <q-btn
              flat
              @click="$router.push('/esqueci')"
            >Esqueci minha senha!
            </q-btn>
            <q-btn
              type="submit"
              color="primary"
              :loading="params.loadingEntrar"
              icon="forward"
            >Entrar
            </q-btn>
          </q-card-actions>
        </q-card>
      </q-form>
    </q-page-container>
  </q-layout>
</template>

<script lang="ts">
import { defineComponent, reactive } from '@vue/composition-api';
import { AxiosResponse, AxiosError } from 'axios';
import { openURL } from 'quasar';
import Vue from 'vue';
import { SessionStorage, Notify } from 'quasar';

export default defineComponent({
  name: 'LoginView',
  setup (props, { root }) {
    const params = reactive({
      loadingEntrar: false,
      form: { username: '', password: '' },
      // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
      backimg: require('./../../assets/sutekidane.jpg')
    });
    function onSubmit () {
      params.loadingEntrar = true;
      let tentativa = 0;
      if (SessionStorage.has('tentativa')) {
        if (SessionStorage.getItem('tentativa') !== null)
          tentativa = Number(SessionStorage.getItem('tentativa'));
        if (tentativa > 6) {
          let valor: number = tentativa / 6;
          valor = valor * 15;
          SessionStorage.set('tentativa', tentativa + 1);
          Notify.create({
            type: 'warning',
            message: 'Número de tentativas excedido! Aguarde ' + String(valor) + ' minutos. Novas tentativas renovam o tempo de espera.'
          });
          params.loadingEntrar = false;
          return;
        }
      }
      root.$axios({
        // eslint-disable-next-line @typescript-eslint/no-unsafe-call,@typescript-eslint/no-unsafe-member-access,@typescript-eslint/restrict-plus-operands
        url: Vue.prototype.$servidor() + '/login',
        method: 'POST',
        data: { username: params.form.username, password: params.form.password }
      })
      .then(function (response: AxiosResponse) {
        if (SessionStorage.has('token')) {
          SessionStorage.remove('token');
        }
        // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
        SessionStorage.set('token', response.data.token);
        SessionStorage.set('nome', params.form.username);
        SessionStorage.set('fullname', response.data.fullname)
        if (SessionStorage.has('tentativa')) {
          SessionStorage.remove('tentativa');
        }
        params.loadingEntrar = false;
        void root.$router.push('/');
      })
      .catch(function (err: AxiosError) {
        console.log(err);
        if (err.code === '404') {
          Notify.create({
            type: 'warning',
            message: 'Usuário ou senha incorretos.'
          });
          if (tentativa) {
            if (tentativa <= 6) {
              SessionStorage.set('tentativa', tentativa + 1);
            }
          }
        } else {
          // eslint-disable-next-line @typescript-eslint/no-unsafe-call,@typescript-eslint/no-unsafe-member-access
          Vue.prototype.$erro(err);
        }
        params.loadingEntrar = false;
      });
    }
    return {
      params,
      onSubmit,
    };
  },
  mounted: function(){
    if (SessionStorage.has('token')){
      this.$router.push('/')
    }
  }
});
</script>

<style>
  .login-card {
    width: 350px;
  }

  .form {
    margin-bottom: 16px;
  }

  .form * {
    margin-right: 4px;
  }

  .dialogo-titulo-aman {
    border-radius: 2px 2px 0 0;
    color: #a9a9a9;
    font-weight: bolder;
    text-align: center;
    font-size: 250% !important;
    text-shadow: 1px 1px 1px #888;
  }

  .dialogo-titulo-lab {
    border-radius: 2px 2px 0 0;
    color: #f16538;
    font-weight: bolder;
    text-align: center;
    font-size: 250% !important;
    text-shadow: 1px 1px 1px #888;
  }
</style>