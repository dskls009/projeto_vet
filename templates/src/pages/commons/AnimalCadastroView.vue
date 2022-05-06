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
          Cadastro de Animal
        </div>
      </div>
      <div class="row">
        <div class="col">
          <q-select
            outlined
            dense
            use-input
            v-model="form.cliente__id"
            :options="data"
            label="Tutor (CPF)"
            option-label="cpf"
            option-value="id"
            emit-value
            map-options
            @filter="filtrar"
            :readonly="edicao"
          />
        </div>
        <div class="col">
          <!-- <q-file outlined dense v-model="foto" label="Foto">
            <template v-slot:prepend>
              <q-icon name="insert_photo" />
            </template>
          </q-file> -->
        </div>
        <div class="col">
          <!-- soh p ajustar o campo -->
        </div>
      </div>
      <div class="row">
        <div class="col">
          <q-input outlined dense v-model="form.rga" label="RGA" />
        </div>
        <div class="col">
          <q-input outlined dense v-model="form.nome" label="Nome" />
        </div>
        <div class="col">
          <q-select
            outlined
            dense
            v-model="form.sexo"
            :options="sexo"
            label="Sexo"
          />
        </div>
      </div>
      <div class="row">
        <div class="col">
          <q-input outlined dense v-model="form.especie" label="Espécie" />
        </div>
        <div class="col">
          <q-input outlined dense v-model="form.raca" label="Raça" />
        </div>
        <div class="col">
          <q-input outlined dense v-model="form.cor" label="Cor" />
        </div>
      </div>
      <div class="row">
        <div class="col">
          <q-input outlined dense v-model="form.peso" label="Peso" />
        </div>
        <div class="col">
          <q-input outlined dense v-model="form.porte" label="Porte" />
        </div>
        <div class="col">
          <!-- ajustando campos -->
        </div>
        </div>
        <div class="row">
        <div class="col">
          <q-checkbox v-model="form.castrado" label="Castrado" />
        </div>
        <div class="col">
          <q-input
            outlined
            dense
            v-model="form.data_castracao"
            label="Data de Castração"
            type="date"
            :disable="!form.castrado"
          />
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
            type="date"
            v-model="form.nascimento"
            label="Data de Nascimento"
          />
        </div>
        <div class="col">
          <q-input
            outlined
            dense
            v-model="form.cartao_vacinacao__descricao"
            label="Cartão de Vacinação"
          />
        </div>
        <div class="col">
          <q-input
            type="textarea"
            outlined
            dense
            v-model="form.cartao_vacinacao__observacao"
            label="Observação"
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
import { save, get } from './../../services/commons/AnimalService';
import { findall } from '../../services/commons/ClienteService';

export default defineComponent({
  name: 'AnimalCadastroView',
  data() {
    return {
      sexo: require('./../../assets/db/sexos.json'),
      form: {
        cartao_vacinacao__descricao: 'Cartão de ',
        castrado: false
      },
      data: [],
      filtro: undefined,
      pk: undefined,
      edicao: false,
      foto: undefined
    };
  },
  methods: {
    voltar_busca: function() {
      this.$router.push('/animal/busca');
    },
    salvar: function() {
      save(this);
    },
    filtrar: function(val, update, abort) {
      this.filtro = val;
      findall(this);
      update(() => {
        this.data = this.data;
      });
    },
    editar: function() {
      get(this);
    }
  },
  mounted: function() {
    if (this.$route.params.id != null) {
      this.pk = this.$route.params.id;
      this.editar();
      this.edicao = true;
    }
  },
  watch: {
    foto: function() {
      this.form.foto = this.foto.name;
    },
    'form.nome': function(){
      this.form.cartao_vacinacao__descricao = 'Cartão de '+this.form.nome
    }
  }
});
</script>

<style>
.col {
  margin: 1px;
}
</style>
