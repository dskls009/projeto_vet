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
          Cadastro de Cliente
        </div>
      </div>
      <div class="row">
        <div class="col">
          <!-- <q-file outlined dense v-model="foto" label="Foto">
            <template v-slot:prepend>
              <q-icon name="insert_photo" />
            </template>
          </q-file> -->
        </div>
        <div class="col">
          <q-select
            outlined
            dense
            v-model="form.genero"
            :options="generos"
            label="Gênero"
            option-value="sigla"
            option-label="nome"
            emit-value
            map-options
            clearable
          />
        </div>
        <div class="col">
          <q-checkbox v-model="form.inadimplente" label="Inadimplente" />
        </div>
      </div>
      <div class="row">
        <div class="col">
          <q-input outlined dense v-model="form.cpf" label="CPF" />
        </div>
        <div class="col">
          <q-input outlined dense v-model="form.nome" label="Nome" />
        </div>
        <div class="col">
          <q-input outlined dense v-model="form.sobrenome" label="Sobrenome" />
        </div>
      </div>
      <div class="row">
        <div class="col">
          <q-input outlined dense v-model="form.email" label="Email" />
        </div>
        <div class="col">
          <q-input
            outlined
            dense
            v-model="form.telefone_1"
            label="Telefone (1)"
          />
        </div>
        <div class="col">
          <q-input
            outlined
            dense
            v-model="form.telefone_2"
            label="Telefone (2)"
          />
        </div>
      </div>
      <endereco-component
        ref="endereco_component"
        @valor="endereco_comp"
      ></endereco-component>
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
import EnderecoComponent from '../../components/EnderecoComponent.vue';
import { save, get } from './../../services/commons/ClienteService';

export default defineComponent({
  name: 'ClienteCadastroView',
  components: { EnderecoComponent },
  data() {
    return {
      generos: require('./../../assets/db/generos.json'),
      form: {
        inadimplente: false
      },
      pk: undefined,
      foto: undefined
    };
  },
  methods: {
    endereco_comp: function(val) {
      if (val) {
        this.form.endereco__endereco = val.endereco;
        this.form.endereco__numero = val.numero;
        this.form.endereco__complemento = val.complemento;
        this.form.endereco__estado = val.estado;
        this.form.endereco__cep = val.cep;
        this.form.endereco__municipio = val.municipio;
        this.form.endereco__bairro = val.bairro;
      }
    },
    voltar_busca: function() {
      this.$router.push('/cliente/busca');
    },
    salvar: function() {
      this.endereco_comp(this.$refs.endereco_component.get());
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
  watch: {
    foto: function() {
      this.form.foto = this.foto.name;
    },
    'form.endereco__id': function() {
      this.$refs.endereco_component.editar({
        cep: this.form.endereco__cep,
        endereco: this.form.endereco__endereco,
        numero: this.form.endereco__numero,
        complemento: this.form.endereco__complemento,
        bairro: this.form.endereco__bairro,
        estado: this.form.endereco__estado,
        municipio: this.form.endereco__municipio
      });
    }
  }
});
</script>

<style>
.col {
  margin: 1px;
}
</style>
