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
          Cadastro de Receita
        </div>
      </div>
      <div class="row">
        <div class="col">
          <q-select
            outlined
            dense
            use-input
            v-model="form.doenca__id"
            :options="data_doenca"
            label="Doença"
            option-label="doenca"
            option-value="id"
            emit-value
            map-options
            @filter="filtrar_doenca"
          />
        </div>
        <div class="col">
          <q-select
            outlined
            dense
            use-input
            v-model="form.medicamento__id"
            :options="data_medicamento"
            label="Medicamento"
            option-label="medicamento"
            option-value="id"
            emit-value
            map-options
            @filter="filtrar_medicamento"
          />
        </div>
        <div class="col">
          <q-file outlined
            dense v-model="form.anexo" label="Anexo" >
            <template v-slot:prepend>
          <q-icon name="attach_file" />
        </template>
      </q-file>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <q-input
            outlined
            dense
            v-model="form.receita"
            label="Receita"
            type="textarea"
          />
        </div>
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
import { save, get } from './../../services/veterinaria/ReceituarioService';
import { findall as findall_medicamento } from './../../services/veterinaria/MedicamentoService';
import { findall as findall_doenca } from './../../services/veterinaria/DoencaService';
import { save as save_base64 } from './../../services/commons/Base64Service';

export default defineComponent({
  name: 'ReceituarioCadastroView',
  data() {
    return {
      form: {
        anexo__base64: undefined,
        anexo: null,
      },
      base64: {
        base64: undefined,
        extensao: undefined
      },
      base64__id: 0,
      data_doenca: [],
      data_medicamento: [],
      filtro_doenca: undefined,
      filtro_medicamento: undefined,
      pk: undefined,
    };
  },
  methods: {
    voltar_busca: function() {
      this.$router.push('/receituario/busca');
    },
    salvar: function() {
      save(this);
    },
    editar: function() {
      get(this);
    },
    factory_anexo(file) {
      return new Promise((resolve, reject) => {
        this.getBase64(file)
          .then(data => {
            this.base64.base64 = data;
            this.base64.extensao = file.name;
            setTimeout(() => {
              resolve(save_base64(this));
            }, 1000);
            setTimeout(() => {
              this.form.anexo__base64 = this.base64__id;
            }, 1500);
          })
          .catch(error => {
            this.$erro(error);
          });
      });
    },
    getBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
      });
    },
    filtrar_medicamento: function(val, update, abort) {
      this.filtro_medicamento = val;
      findall_medicamento(this)
      update(() => {
        this.data_medicamento = this.data_medicamento;
      });
    },
    filtrar_doenca: function(val, update, abort) {
      this.filtro_medicamento = val;
      findall_doenca(this)
      update(() => {
        this.data_doenca = this.data_doenca;
      });
    },
  },
  mounted: function() {
    if (this.$route.params.id != null) {
      this.pk = this.$route.params.id;
      this.editar();
    }
  },
  watch: {
    'form.anexo': function(){
      if (this.form.anexo && this.form.anexo != undefined && this.form.anexo != null){
        this.factory_anexo(this.form.anexo)
      }
    }
  }
});
</script>

<style>
.col {
  margin: 1px;
}
</style>
