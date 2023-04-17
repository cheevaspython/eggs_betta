<template>
  <form action="" style="width: 1000px">
    <div class="modal-card" style="width: 900px; height: 95vh">
      <header class="modal-card-head" style="background-color: #c3c3c3; text-align: center">
        <p class="modal-card-title" style="color: whitesmoke; font-size: 30px; font-weight: 900">Создание продавца</p>
        <button
          type="button"
          class="delete"
          @click="$emit('close')"/>
      </header>
      <section class="modal-card-body is-fullwidth flexbox flexbox__column">
        <h4 class="title has-text-centered border">Данные продавца</h4>
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
        <div class="flexbox__row flexbox__space-between input-border">
          <div style="margin-left: 10px">Регион</div>
          <b-field class="my-b-input">
            <b-input placeholder="Введите регион" rounded v-model="region"></b-input>
          </b-field>
        </div>
        <div class="flexbox__row flexbox__space-between input-border">
          <div style="margin-left: 10px">Адрес производства</div>
          <b-field class="my-b-input">
            <b-input placeholder="Введите адрес" rounded v-model="prodAddress1"></b-input>
          </b-field>
        </div>
        <div class="flexbox__row flexbox__space-between input-border" v-show="prodAddress1">
          <div style="margin-left: 10px">Адрес производства</div>
          <b-field class="my-b-input">
            <b-input placeholder="Введите дополнительный адрес" rounded v-model="prodAddress2"></b-input>
          </b-field>
        </div>
        <div class="flexbox__row flexbox__space-between input-border" v-show="prodAddress2">
          <div style="margin-left: 10px">Адрес производства</div>
          <b-field class="my-b-input">
            <b-input placeholder="Введите дополнительный адрес" rounded v-model="prodAddress3"></b-input>
          </b-field>
        </div>
        <div class="flexbox__row input-border flexbox__space-between">
          <div class="drop">
            <b-dropdown :triggers="['hover']" aria-role="list">
              <template #trigger>
                <b-button
                  v-model="manager"  
                  label="Выберите менеджера"
                  type="is-success is-light"
                  icon-right="menu-down"
                  rounded />
              </template>

              <b-dropdown-item v-for="user in users" :key="user.id" @click="selectManager(user)" v-show="user.first_name && user.last_name && user.role == 1 || user.role == 3">
                {{ user.first_name + ' ' + user.last_name }}
              </b-dropdown-item>
            </b-dropdown>
          </div>
          <div class="drop flexbox__end" style="margin-right: 10px; width: 33%;">
            <div v-if="manager">{{ manager.first_name + ' ' + manager.last_name }}</div>
          </div>
        </div>
        <!-- <div class="flexbox__row flexbox__space-between input-border">
          <div style="margin-left: 10px">Тип оплаты</div>
          <b-field class="my-b-input flexbox__end flexbox__row">
            <div class="pay-type">С НДС</div>
            <div class="pay-type">Без НДС</div>
          </b-field>
        </div> -->
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
          @click="createSeller"/>
        <b-button
          label="Закрыть"
          @click="$emit('close')"/>
      </footer>
    </div>
  </form>
</template>

<script>
export default {
  name: "ModalCreateSellerForm",
  data() {
    return {
      loading: false,
      name: null,
      inn: null,
      generalManager: null,
      phone: null,
      email: null,
      payType: null,
      comment: null,
      contactPerson: null,
      region: null,
      bankName: null,
      bicBank: null,
      corAccount: null,
      customersPayAccount: null,
      legalAddress: null,
      physicalAddress: null,
      prodAddress1: null,
      prodAddress2: null,
      prodAddress3: null,
      users: null,
      manager: null
    }
  },
  methods: {
    async createSeller() {
      if (!this.name) {
        return alert('Вы не ввели название')
      }
      if (!this.inn) {
        return alert('Вы не ввели ИНН')
      }
      if (!this.generalManager) {
        return alert('Вы не ввели ФИО ген. директора')
      }
      if (!this.phone) {
        return alert('Вы не ввели контакный номер телефона')
      }
      if (!this.email) {
        return alert('Вы не ввели почту')
      }
      if (!this.region) {
        return alert('Вы не ввели регион')
      }
      if (!this.prodAddress1) {
        return alert('Вы не ввели адрес производства')
      }
      if (!this.manager) {
        return alert('Вы не выбрали менеджера')
      }

      const seller = {
        name: this.name,
        inn: this.inn,
        general_manager: this.generalManager,
        phone: this.phone,
        email: this.email,
        // pay_type: this.payType,
        comment: this.comment,
        contact_person: this.contactPerson,
        region: this.region,
        prod_address_1: this.prodAddress1,
        prod_address_2: this.prodAddress2,
        prod_address_3: this.prodAddress3,
        bank_name: this.bankName,
        bic_bank: this.bicBank,
        cor_account: this.corAccount,
        customers_pay_account: this.customersPayAccount,
        legal_address: this.legalAddress,
        physical_address: this.physicalAddress,
        manager: this.manager.id,
        manager_details: this.manager.first_name + ' ' + this.manager.last_name
      }
      this.loading = true
      const postRequest = await this.$store.dispatch('ca/postSeller', seller)
        .finally(() => this.loading = false)
      if (postRequest) {
        this.$emit('close')
        this.update()
      }
    },
    update() {
      this.$store.dispatch('ca/getSellers')
      this.$store.dispatch('bid/getOwnerTasks')
      this.$store.dispatch('user/getUserNotifications')
    },
    selectManager(user) {
      this.manager = user
    },
    getBackgroundColor(payType) {
      if (payType == this.payType) {
        return '#48c78e'
      }
      else {
        return '#fff'
      }
    }
  },
  async created() {
    await this.$store.dispatch('ca/getAllUsers')
    this.users = this.$store.state.ca.allUsers
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

.input-border {
  height: 40px;
  border: solid 2px #ebebeb;
  border-radius: 20px;
  width: 100%;
  margin-bottom: 5px;
  align-items: center;
}

.pay-type {
  border: solid 2px #ebebeb;
  height: 40px;
  width: 50%;
  text-align: center;
  cursor: pointer;
  border-radius: 20px;
  align-content: center;
}

.my-b-input {
  width: 75%;
}

.drop {
  display: flex;
  width: 33%;
  height: 40px;
  align-items: center;
}

.border {
  height: 40px;
  border: solid #f8f8f8 2px;
  border-radius: 20px;
  background-color: #f5f5f5;
}
</style>