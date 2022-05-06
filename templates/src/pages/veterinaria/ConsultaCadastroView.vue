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
          Registro de Consulta
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
          <q-input outlined dense v-model="form.descricao" label="Descrição" />
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
            v-model="form.data_inicio"
            label="Data de Início"
            type="date"
          />
        </div>
        <div class="col">
          <q-input
            outlined
            dense
            v-model="form.hora_inicio"
            label="Hora de Início"
            type="time"
          />
        </div>
        <div class="col">
          <q-input
            outlined
            dense
            v-model="form.data_fim"
            label="Data de Término"
            type="date"
          />
        </div>
        <div class="col">
          <q-input
            outlined
            dense
            v-model="form.hora_fim"
            label="Hora de Término"
            type="time"
          />
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
          <q-btn
            label="Medicamento Administrado"
            flat
            class="full-width"
            icon-right="medication"
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
import { save, get } from './../../services/veterinaria/ConsultaService';
import { findall } from './../../services/commons/AnimalService';

export default defineComponent({
  name: 'ConsultaCadastroView',
  data() {
    return {
      form: {},
      data: [],
      preenchido: false,
      animal: undefined,
      pk: undefined,
    };
  },
  methods: {
    voltar_busca: function() {
      this.$router.push(`/consulta/busca/${this.$route.params.animal}`);
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
      if (this.$route.params.animal != null){
          this.form.animal__id = this.$route.params.animal
          this.preenchido = true
      }
      if (this.$route.params.id != null) {
      this.pk = this.$route.params.id;
      this.editar();
    }
  },
  watch: {
  }
});
</script>

<style>
.col {
  margin: 1px;
}
</style>
