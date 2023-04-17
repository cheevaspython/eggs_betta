<template>
  <form action="" style="width: 1000px">
    <div class="modal-card" style="width: 900px; height: 95vh">
      <header class="modal-card-head" style="background-color: #c3c3c3; text-align: center">
        <p class="modal-card-title" style="color: whitesmoke; font-size: 30px; font-weight: 900">Создание логиста</p>
        <button
          type="button"
          class="delete"
          @click="$emit('close')"/>
      </header>
      <section class="modal-card-body is-fullwidth flexbox flexbox__column">

        <h4 class="title has-text-centered border">Данные логиста</h4>
        <div class="flexbox__row flexbox__space-between input-border">
          <div style="margin-left: 10px">Название</div>
          <b-field class="my-b-input">
            <b-input placeholder="Введите название" rounded v-model="name"></b-input>
          </b-field>
        </div>
        <div class="flexbox__row flexbox__space-between input-border">
          <div style="margin-left: 10px">ИНН</div>
          <b-field class="my-b-input">
            <b-input placeholder="Введите ИНН" rounded v-model="inn"></b-input>
          </b-field>
        </div>
        <div class="flexbox__row flexbox__space-between input-border">
          <div style="margin-left: 10px">Генеральный директор</div>
          <b-field class="my-b-input">
            <b-input placeholder="Введите ФИО" rounded v-model="generalManager"></b-input>
          </b-field>
        </div>
        <div class="flexbox__row flexbox__space-between input-border">
          <div style="margin-left: 10px">Номер телефона</div>
          <b-field class="my-b-input">
            <b-input placeholder="Введите номер" rounded v-model="phone"></b-input>
          </b-field>
        </div>
        <div class="flexbox__row flexbox__space-between input-border">
          <div style="margin-left: 10px">Почта</div>
          <b-field class="my-b-input">
            <b-input placeholder="Введите почту" rounded v-model="email"></b-input>
          </b-field>
        </div>
        <div class="flexbox__row flexbox__space-between input-border">
          <div style="margin-left: 10px">Контактное лицо</div>
          <b-field class="my-b-input">
            <b-input placeholder="Введите ФИО" rounded v-model="contactPerson"></b-input>
          </b-field>
        </div>
        <!-- <div class="flexbox__row flexbox__space-between input-border">
          <div style="margin-left: 10px">Регион</div>
          <b-field class="my-b-input">
            <b-input placeholder="Введите регион" rounded v-model="region"></b-input>
          </b-field>
        </div> -->
        <div class="flexbox__row">
          <div class="flexbox__row flexbox__space-between input-border">
            <div style="margin-left: 10px">Тип оплаты доставки</div>
            <div style="width: 50%" class="flexbox__row">
              <div class="payType" @click="payType = 20" v-bind:style="{'background-color': getBackgroundColor(20)}">С НДС</div>
              <div class="payType" @click="payType = 0" v-bind:style="{'background-color': getBackgroundColor(0)}">Без НДС</div>
            </div>
          </div>
        </div>
        <b-field>
          <b-input placeholder="Комментарий" type="textarea" rounded v-model="comment"></b-input>
        </b-field>

        <h4 class="title has-text-centered border">Реквизиты</h4>
        <div class="flexbox__row flexbox__space-between input-border">
          <div style="margin-left: 10px">Название банка</div>
          <b-field class="my-b-input">
            <b-input placeholder="Введите название" rounded v-model="bankName"></b-input>
          </b-field>
        </div>
        <div class="flexbox__row flexbox__space-between input-border">
          <div style="margin-left: 10px">БИК банка</div>
          <b-field class="my-b-input">
            <b-input placeholder="Введите БИК" rounded v-model="bicBank"></b-input>
          </b-field>
        </div>
        <div class="flexbox__row flexbox__space-between input-border">
          <div style="margin-left: 10px">Кор. счет банка</div>
          <b-field class="my-b-input">
            <b-input placeholder="Введите номер счета банка" rounded v-model="corAccount"></b-input>
          </b-field>
        </div>
        <div class="flexbox__row flexbox__space-between input-border">
          <div style="margin-left: 10px">Счет клиента</div>
          <b-field class="my-b-input">
            <b-input placeholder="Введите номер счета клиента" rounded v-model="customersPayAccount"></b-input>
          </b-field>
        </div>
        <div class="flexbox__row flexbox__space-between input-border">
          <div style="margin-left: 10px">Юридический адрес</div>
          <b-field class="my-b-input">
            <b-input placeholder="Введите адрес" rounded v-model="legalAddress"></b-input>
          </b-field>
        </div>
        <div class="flexbox__row flexbox__space-between input-border">
          <div style="margin-left: 10px">Фактический адрес</div>
          <b-field class="my-b-input">
            <b-input placeholder="Введите адрес" rounded v-model="physicalAddress"></b-input>
          </b-field>
        </div>
      </section>
      <footer class="modal-card-foot is-justify-content-flex-end">
        <b-button
          label="Создать"
          :loading="loading"
          type="is-success"
          @click="createLogic"/>
        <b-button
          label="Закрыть"
          @click="$emit('close')"/>
      </footer>
    </div>
  </form>
</template>

<script>
export default {
  name: "ModalCreateLogicForm",
  data() {
    return {
      loading: false,
      name: null,
      inn: null,
      generalManager: null,
      phone: null,
      email: null,
      payType: 20,
      comment: null,
      contactPerson: null,
      region: null,
      bankName: null,
      bicBank: null,
      corAccount: null,
      customersPayAccount: null,
      legalAddress: null,
      physicalAddress: null
    }
  },
  methods: {
    async createLogic() {
      const logic = {
        name: this.name,
        inn: this.inn,
        general_manager: this.generalManager,
        phone: this.phone,
        email: this.email,
        // pay_type: this.payType,
        comment: this.comment,
        contact_person: this.contactPerson,
        bank_name: this.bankName,
        bic_bank: this.bicBank,
        cor_account: this.corAccount,
        customers_pay_account: this.customersPayAccount,
        legal_address: this.legalAddress,
        physical_address: this.physicalAddress
      }
      this.loading = true
      await this.$store.dispatch('ca/postLogic', logic)
        .finally(() => this.loading = false, setTimeout(this.update, 1000))
      this.$emit('close')
    },
    update() {
      this.$store.dispatch('ca/getLogists')
      this.$store.dispatch('bid/getOwnerTasks')
      this.$store.dispatch('user/getUserNotifications')
    },
    getBackgroundColor(payType) {
      if (payType == this.payType) {
        return '#48c78e'
      }
      else {
        return '#fff'
      }
    },
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
  &__space-between{
    justify-content: space-between;
  }
}

.card {
  width: 100%;

  &__row {
    display: flex;
    font-size: 16px;
    justify-content: space-between;
    margin-bottom: .5rem;
    border-bottom: solid #f5f5f5 2px;
  }
  &__info {
    overflow-wrap: break-word;
    font-size: 16px;
    max-width: 700px;
    font-weight: 500;
    margin-left: 1rem;
  }
}

.payType {
  display: inline-flex;
  width: 50%;
  border: solid 2px #f5f5f5;
  font-weight: 400;
  justify-content: center;
  border-radius: 20px;
  padding: 5px;
  cursor: pointer;
}

.input-border {
  border: solid 2px #ebebeb;
  border-radius: 20px;
  width: 100%;
  height: 40px;
  margin-bottom: 5px;
  align-items: center;
}

.my-b-input {
  width: 75%;
}

.border {
  height: 40px;
  border: solid #f8f8f8 2px;
  border-radius: 5px;
  background-color: #f5f5f5;
}
</style>