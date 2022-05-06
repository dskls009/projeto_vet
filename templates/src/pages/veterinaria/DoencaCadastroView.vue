<template>
  <q-page padding class="full-width">
    <q-form @submit="salvar">
      <div class="row">
        <div class="col">
          <q-btn
            label="Voltar"
            color="negative"
            flat
            icon="arrow_back"
            @click="voltar_busca"
          />
        </div>
      </div>
      <div class="row">
        <div class="col text-h5 text-weight-light">
          Cadastro de Doença
        </div>
      </div>
      <div class="row">
        <div class="col">
          <q-input outlined dense v-model="form.doenca" label="Doença" />
        </div>
        <div class="col">
          <q-checkbox v-model="form.cronica" label="Crônica" />
        </div>
        <div class="col">
          <!-- ajustando campos -->
        </div>
      </div>
      <div class="row">
        <div class="col">
          <q-input
            outlined
            dense
            v-model="form.observacao"
            label="Observação"
            type="textarea"
          />
        </div>
        <div class="col">
          <!-- ajustando campos -->
        </div>
        <div class="col">
          <!-- ajustando campos -->
        </div>
      </div>
      <div class="column items-end">
        <div class="col">
          <q-btn label="Salvar" flat icon-right="done" type="submit" />
        </div>
      </div>
    </q-form>
  </q-page>
</template>

<script>
import { defineComponent } from '@vue/composition-api';
import { save, get } from './../../services/veterinaria/DoencaService';
import { SessionStorage } from 'quasar';

export default defineComponent({
  name: 'VacinaCadastroView',
  data() {
    return {
      form: {
          cronica: false,
      },
      data: [],
      pk: undefined
    };
  },
  methods: {
    voltar_busca: function() {
      this.$router.push('/doenca/busca');
    },
    salvar: function() {
      save(this);
    },
    editar: function() {
      get(this);
    }
  },
  mounted: function() {
    if (this.$route.params.id != null) {
      this.pk = this.$route.params.id;
      this.editar();
    }
  },
  watch: {}
});
</script>

<style>
.col {
  margin: 1px;
}
</style>
