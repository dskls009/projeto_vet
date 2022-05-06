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
          Cadastro de Medicamento
        </div>
      </div>
      <div class="row">
        <div class="col">
          <q-input
            outlined
            dense
            v-model="form.medicamento"
            label="Medicamento"
          />
        </div>
        <div class="col">
          <q-input
            outlined
            dense
            v-model="form.quantidade"
            label="Quantidade"
          />
        </div>
        <div class="col">
          <q-input
            outlined
            dense
            v-model="form.unidade_medida"
            label="Unidade de Medida"
          />
        </div>
      </div>
      <div class="row">
        <div class="col">
          <!-- <q-uploader
            :factory="factory_bula"
            no-thumbnails
            flat
            bordered
            label="Bula"
            @failed="uploadFailed"
          /> -->
          <q-file outlined
            dense v-model="form.bula" label="Bula" >
            <template v-slot:prepend>
          <q-icon name="description" />
        </template>
      </q-file>
        </div>
        <div class="col">
          <!-- <q-uploader
            :factory="factory_anexo"
            flat
            bordered
            label="Anexo"
            @failed="uploadFailed"
          /> -->
          <q-file outlined
            dense v-model="form.anexo" label="Anexo" >
            <template v-slot:prepend>
          <q-icon name="image" />
        </template>
      </q-file>
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
import { save, get } from './../../services/veterinaria/MedicamentoService';
import { save as save_base64 } from './../../services/commons/Base64Service';

export default defineComponent({
  name: 'MedicamentoCadastroView',
  data() {
    return {
      form: {
        bula__base64: undefined,
        anexo__base64: undefined,
        bula: null,
        anexo: null,
      },
      base64: {
        base64: undefined,
        extensao: undefined
      },
      base64__id: 0,
      pk: undefined,
      bula: undefined,
      anexo: undefined
    };
  },
  methods: {
    voltar_busca: function() {
      this.$router.push('/medicamento/busca');
    },
    salvar: function() {
      save(this);
    },
    editar: function() {
      get(this);
    },
    factory_bula(file) {
      return new Promise((resolve, reject) => {
        this.getBase64(file)
          .then(data => {
            this.base64.base64 = data;
            this.base64.extensao = file.name;
            setTimeout(() => {
              resolve(save_base64(this));
            }, 1000);
            setTimeout(() => {
              this.form.bula__base64 = this.base64__id;
            }, 1500);
          })
          .catch(error => {
            this.$erro(error);
          });
      });
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
    }
  },
  mounted: function() {
    if (this.$route.params.id != null) {
      this.pk = this.$route.params.id;
      this.editar();
    }
  },
  watch: {
    'form.bula': function(){
      if (this.form.bula && this.form.bula != undefined && this.form.bula != null){
        this.factory_bula(this.form.bula)
      }
    },
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
