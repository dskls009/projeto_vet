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
          Registro de Vacinação
        </div>
      </div>
      <div class="row">
        <div class="col">
          <q-select
            outlined
            dense
            use-input
            v-model="form.animal__id"
            :options="data"
            label="Animal"
            option-label="nome"
            option-value="id"
            emit-value
            map-options
            :readonly="preenchido"
            @filter="filtrar"
          />
        </div>
        <div class="col">
          <q-input outlined dense v-model="form.vacina" label="Vacina" />
        </div>
        <div class="col">
          <q-input outlined dense v-model="form.dose" label="Dose" />
        </div>
      </div>
      <div class="row">
        <div class="col">
          <q-input
            outlined
            dense
            v-model="form.data_aplicacao"
            label="Data de Aplicação"
            type="date"
          />
        </div>
        <div class="col">
          <q-input
            outlined
            dense
            v-model="form.proxima_dose"
            label="Data da Próxima Dose"
            type="date"
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
import { save, get } from './../../services/veterinaria/VacinaService';
import { findall } from './../../services/commons/AnimalService';
import { SessionStorage } from 'quasar';

export default defineComponent({
  name: 'VacinaCadastroView',
  data() {
    return {
      form: {},
      data: [],
      preenchido: false,
      animal: undefined,
      pk: undefined
    };
  },
  methods: {
    voltar_busca: function() {
      if (SessionStorage.has('cliente')) {
        this.$router.push(`/animal/busca/${SessionStorage.getItem('cliente')}`);
      } else {
        this.$router.push('/animal/busca');
      }
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
    if (this.$route.params.animal != null) {
      this.form.animal__id = this.$route.params.animal;
      this.preenchido = true;
    }
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
