<template>
  <q-page padding class="full-width">
    <div class="q-pa-md">
      <q-form>
        <div class="row">
          <div class="col">
            <p style="font-size: 30px">
              Cadastro de Animal <q-btn round flat color="primary" icon="add" />
            </p>
          </div>
        </div>
        <div class="row">
          <div class="col">
            <q-select
              filled
              dense
              use-input
              v-model="form.tutor__id"
              :options="data_tutor"
              label="Tutor (CPF)"
              option-label="cpf"
              option-value="id"
              emit-value
              map-options
              @filter="filtrar"
              :disable="salvou"
            />
          </div>
        </div>
        <div class="row">
          <div class="col">
            <q-input
              filled
              dense
              v-model="form.rga"
              label="RGA"
              :disable="salvou"
            />
          </div>
          <div class="col">
            <q-input
              filled
              dense
              v-model="form.nome"
              label="Nome"
              :disable="salvou"
            />
          </div>
          <div class="col">
            <q-checkbox
              v-model="form.castrado"
              label="Castrado"
              :disabled="salvou"
            />
          </div>
        </div>
        <div class="row">
          <div class="col">
            <q-input
              filled
              dense
              v-model="form.especie"
              label="Espécie"
              :disable="salvou"
            />
          </div>
          <div class="col">
            <q-input
              filled
              dense
              v-model="form.raca"
              label="Raça"
              :disable="salvou"
            />
          </div>
          <div class="col">
            <q-input
              filled
              dense
              v-model="form.cor"
              label="Cor"
              :disable="salvou"
            />
          </div>
        </div>
        <div class="row">
          <div class="col">
            <q-input
              filled
              dense
              v-model="form.nascimento"
              label="Data de Nascimento"
              :disable="salvou"
              type="date"
            />
          </div>
          <div class="col">
            <q-input
              filled
              dense
              v-model="form.peso"
              label="Peso"
              :disable="salvou"
            />
          </div>
          <div class="col">
            <q-input
              filled
              dense
              v-model="form.porte"
              label="Porte"
              :disable="salvou"
            />
          </div>
        </div>
        <div class="column items-end">
          <div class="col-4 offset-8">
            <q-btn color="primary" label="Salvar" @click="save_animal" />
          </div>
        </div>
        <div class="row">
          <div class="col">
            <p style="font-size: 30px">
              Condições Especiais
              <q-btn
                round
                flat
                color="primary"
                icon="add"
                @click="nova_condicao"
              />
            </p>
          </div>
        </div>
        <div v-if="salvou">
          <div class="row">
            <div class="col">
              <q-input
                filled
                dense
                v-model="form_condicao.descricao"
                label="Descrição"
              />
            </div>
            <div class="col">
              <q-input
                filled
                dense
                v-model="form_condicao.aquisicao"
                type="date"
                label="Data de Aquisição"
              />
            </div>
            <div class="col">
              <q-input
                filled
                dense
                v-model="form_condicao.cura"
                type="date"
                label="Data de Cura"
              />
            </div>
          </div>
          <div class="row">
            <div class="col-8">
              <q-input
                filled
                dense
                v-model="form_condicao.observacao"
                label="Observação"
              />
            </div>
            <div class="col">
              <q-checkbox
                filled
                v-model="form_condicao.cronica"
                label="Crônica"
              />
            </div>
          </div>
          <div class="column items-end">
            <div class="col-4 offset-8">
              <q-btn color="primary" label="Salvar" @click="save_condicao" />
            </div>
          </div>
        </div>
      </q-form>
    </div>
  </q-page>
</template>

<script>
import { Notify } from 'quasar'
import { findall as tutor_findall } from './../../services/commons/ClienteService';
import {
  findall as animal_findall,
  save as animal_save
} from './../../services/commons/AnimalService';
import { save as condicao_save } from '../../services/veterinaria/CondicaoEspecialService';

export default {
  name: 'CadastroAnimalView',
  props: ['tutor'],
  data() {
    return {
      salvou: false,
      get_animal: {},
      animal__id: 0,
      form: {
        castrado: false
      },
      form_condicao: {
        cronica: false
      },
      filtro_tutor: undefined,
      data_tutor: []
    };
  },
  methods: {
    load_tutor: function() {
      tutor_findall(this);
    },
    filtrar: function(val, update, abort) {
      this.filtro_tutor = val;
      tutor_findall(this);
      update(() => {
        this.data_tutor = this.data_tutor;
      });
    },
    save_animal: function() {
        animal_save(this);
      if (this.form_condicao.animal__id === 0){
        this.erro_ao_criar()
        }
        else {
            this.salvou = true;
        }
          
      
    },
    erro_ao_criar () {
      Notify.create('Ocorreu um erro! Verifique os dados preenchidos!')
    },
    save_condicao: function() {
      condicao_save(this);
    },
    nova_condicao: function() {
      this.form_condicao = {
        animal__id: this.animal__id,
        cronica: false
      };
    }
  },
  mounted: function() {
    this.load_tutor();
  },
  watch: {
    salvou: function(val) {
      this.salvou = val;
    },
    get_animal: function(val){
        this.animal__id = val['id']
        this.form_condicao.animal__id = this.animal__id
        console.log('deu tudo certo pelo amor de deus')
    }
  }
};
</script>
