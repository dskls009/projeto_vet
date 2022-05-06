<template>
  <div>
    <div class="row">
      <div class="col">
        <q-input outlined dense label="CEP" v-model="form.cep"></q-input>
      </div>
      <div class="col">
        <!-- soh pra encurtar a linha do cep direitinho -->
      </div>
      <div class="col">
        <!-- soh pra encurtar a linha do cep direitinho -->
      </div>
    </div>
    <div class="row">
      <div class="col">
        <q-input
          outlined
          dense
          label="Logradouro"
          v-model="form.endereco"
        ></q-input>
      </div>
      <div class="col">
        <q-input
          outlined
          dense
          label="Número"
          v-model="form.numero"
        ></q-input>
      </div>
      <div class="col">
        <q-input
          outlined
          dense
          label="Complemento"
          v-model="form.complemento"
        ></q-input>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <q-input outlined dense label="Bairro" v-model="form.bairro"></q-input>
      </div>
      <div class="col">
        <q-input
          outlined
          dense
          label="Município"
          v-model="form.municipio"
        ></q-input>
      </div>
      <div class="col">
        <q-select
          outlined
          dense
          label="Estado"
          v-model="form.estado"
          option-value="sigla"
          option-label="sigla"
          :options="estados"
          emit-value
          map-options
          clearable
        ></q-select>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EnderecoComponent',
  data() {
    return {
      form: {},
      estados: require('./../assets/db/estados.json')
    };
  },
  methods: {
    editar: function(val) {
      this.form = val;
    },
    novo: function() {
      this.form = {};
    },
    get: function() {
      return this.form;
    }
  },
  watch: {
    form: function(val) {
      if (val) {
        this.$emit('valor', val);
      }
    },
    'form.cep': function(val) {
      if (val !== null && val !== undefined && val.length === 8) {
        this.$axios({
          method: 'GET',
          url: `https://viacep.com.br/ws/${val}/json/`
        }).then(response => {
          this.form.cep = response.data.cep;
          this.form.endereco = response.data.logradouro;
          this.form.complemento = response.data.complemento;
          this.form.bairro = response.data.bairro;
          this.form.municipio = response.data.localidade;
          this.form.estado = response.data.uf;
        });
      }
    }
  }
};
</script>
