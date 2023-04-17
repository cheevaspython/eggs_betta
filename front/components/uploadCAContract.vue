<template>
	<form action="" style="width: 1000px">
    <div class="modal-card" style="width: 900px; height: 350px">
      <header class="modal-card-head" style="background-color: #c3c3c3; text-align: center">
        <p class="modal-card-title" style="color: whitesmoke; font-size: 30px; font-weight: 900">Загрузка Договора</p>
        <button
        type="button"
        class="delete"
        @click="$emit('close')"/>
      </header>
      <section class="modal-card-body is-fullwidth">
        <div class="upload">
          <div>Договор</div>
          <div v-show="contract" class="rdy-to-download">Файл готов к загрузке</div>
          <div v-show="!contract" class="hint">Нажмите чтобы загрузить</div>
          <input style="padding-bottom: 10px; z-index: 100;" accept=".pdf" type="file" id="contract" ref="contract" @change="previewContract"/>
        </div>
      </section>
      <footer class="modal-card-foot is-justify-content-flex-end">
        <b-button
          label="Загрузить"
          type="is-success"
          @click="uploadContract"/>
        <b-button
          label="Закрыть"
          @click="$emit('close')"/>
      </footer>
    </div>
  </form>
</template>
    
<script>
export default {
	name: "uploadCAContract",
	props: ['trader'],
  data() {
    return {
      contract: null
    }
  },
  methods: {
    previewContract() {
      this.contract = this.$refs.contract.files[0]
    },
    uploadContract() {
      const documentContractId = this.trader.documents_contract
      const formData = new FormData()
      if (this.contract) {
        formData.append('contract', this.contract)
      }
      this.$store.dispatch('ca/documentsCotract', [formData, documentContractId]) 
      this.$emit('close')
    }
  },
  created() {
    // console.log(this.trader)
  }
}
</script>
    
<style lang="scss" scoped>
form {
  font-family: 'Montserrat';
}

.flexbox {
  display: flex;

  &__column {
    flex-direction: column;
    flex-flow: column;
  }
  &__row {
    flex-direction: row;
    flex-flow: row;
    display: inline-flex;
  }
  &__start {
    justify-content: flex-start;
  }
  &__center {
    justify-content: center;
  }
  &__end {
    justify-content: flex-end;
  }
  &__space-between {
    justify-content: space-between;
  }
  &__space-around {
    justify-content: space-around;
  }
}

.card {
  float: left;

  &__row {
    display: flex;
    justify-content: space-between;
    margin-bottom: .5rem;
    border-bottom: solid #f5f5f5 2px;
  }

  &__info {
    overflow-wrap: break-word;
    max-width: 500px;
    font-weight: 500;
    margin-left: 1rem;
  }
  
  &__button-wrapper{
    margin-top: 20px;
    display: flex;
    justify-content: center;
  }
}

.upload {
  height: 30px;
  width: 100%;
  border: solid 2px #ebebeb;
  border-radius: 20px;
  margin-bottom: 10px;
  padding-left: 15px;
  cursor: pointer;

  &:hover {
    background-color: #f5f5f5;
  }
}

.hint {
  color: #cdcdcd;
  margin-left: 10px;
}

.rdy-to-download {
  margin-left: 10px;
  color: green;
}
</style>
    