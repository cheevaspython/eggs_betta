<template>
  <form action="" style="width: 1000px">
    <div class="modal-card" style="width: 900px; height: 95vh">
      <header class="modal-card-head" style="background-color: #c3c3c3; text-align: center">
        <p class="modal-card-title" style="color: whitesmoke; font-size: 30px; font-weight: 900">Создание покупателя</p>
        <button
          type="button"
          class="delete"
          @click="$emit('close')"/>
      </header>
      <section class="modal-card-body is-fullwidth flexbox flexbox__column">
        <h4 class="title has-text-centered border">Данные покупателя</h4>
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
          <div style="margin-left: 10px">Лимит задолженности</div>
          <b-field class="my-b-input">
            <b-input placeholder="Введите сумму безналичной задолженности" rounded v-model="limit"></b-input>
          </b-field>
        </div>
        <div class="flexbox__row flexbox__space-between input-border">
          <div style="margin-left: 10px">Лимит задолженности</div>
          <b-field class="my-b-input">
            <b-input placeholder="Введите сумму наличной задолженности" rounded v-model="limitCash"></b-input>
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
          <div style="margin-left: 10px">Адрес склада</div>
          <b-field class="my-b-input">
            <b-input placeholder="Введите адрес" rounded v-model="wharehouseAddress1"></b-input>
          </b-field>
        </div>
        <div class="flexbox__row flexbox__space-between input-border" v-show="wharehouseAddress1">
          <div style="margin-left: 10px">Адрес склада</div>
          <b-field class="my-b-input">
            <b-input placeholder="Введите дополнительный адрес" rounded v-model="wharehouseAddress2"></b-input>
          </b-field>
        </div>
        <div class="flexbox__row flexbox__space-between input-border" v-show="wharehouseAddress2">
          <div style="margin-left: 10px">Адрес склада</div>
          <b-field class="my-b-input">
            <b-input placeholder="Введите дополнительный адрес" rounded v-model="wharehouseAddress3"></b-input>
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

              <b-dropdown-item v-for="user in users" :key="user.id" @click="selectManager(user)" v-show="user.first_name && user.last_name && user.role == 2 || user.role == 3">
                {{ user.first_name + ' ' + user.last_name }}
              </b-dropdown-item>
            </b-dropdown>
          </div>
          <div class="drop flexbox__end" style="margin-right: 10px; width: 33%;">
            <div v-if="manager">{{ manager.first_name + ' ' + manager.last_name }}</div>
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
          @click="createBuyer"/>
        <b-button
          label="Закрыть"
          @click="$emit('close')"/>
      </footer>
    </div>
  </form>
</template>

<script>
export default {
  name: "ModalCreateBuyerForm",
  data() {
    return {
      loading: false,
      name: null,
      inn: null,
      generalManager: null,
      phone: null,
      email: null,
      payType: 0,
      comment: null,
      contactPerson: null,
      region: null,
      bankName: null,
      bicBank: null,
      corAccount: null,
      customersPayAccount: null,
      legalAddress: null,
      physicalAddress: null,
      wharehouseAddress1: null,
      wharehouseAddress2: null,
      wharehouseAddress3: null,
      limit: null,
      limitCash: null,
      users: null,
      manager: null
    }
  },
  methods: {
    async createBuyer() {
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
      if (!this.wharehouseAddress1) {
        return alert('Вы не ввели адрес склада')
      }
      if (!this.manager) {
        return alert('Вы не выбрали менеджера')
      }

      const buyer = {
        name: this.name,
        inn: this.inn,
        general_manager: this.generalManager,
        phone: this.phone,
        email: this.email,
        // pay_type: this.payType,
        pay_limit: parseFloat(this.limit),
        pay_limit_cash: parseFloat(this.limitCash),
        comment: this.comment,
        contact_person: this.contactPerson,
        region: this.region,
        warehouse_address_1: this.wharehouseAddress1,
        warehouse_address_2: this.wharehouseAddress2,
        warehouse_address_3: this.wharehouseAddress3,
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
      const request = await this.$store.dispatch('ca/postBuyer', buyer)
        .finally(() => this.loading = false, setTimeout(this.update, 1000))
      if (!request) { 
        return 
      }
      this.$emit('close')
    },
    update() {
      this.$store.dispatch('ca/getBuyers')
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
      else return '#fff'
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

.input-border {
  border: solid 2px #ebebeb;
  border-radius: 20px;
  width: 100%;
  height: 40px;
  margin-bottom: 5px;
  align-items: center;
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

.my-b-input {
  width: 75%;
}

.check {
  height: 30px;
  text-align: center;
  border: solid 3px #f3f3f3;
  border-radius: 5px;
  background-color: #fff;
  padding: 0 10px;
  margin-bottom: 10px;
  cursor: pointer;
}

.border {
  height: 40px;
  border: solid #f8f8f8 2px;
  font-weight: 300;
  border-radius: 20px;
  background-color: #f5f5f5;
}

.drop {
  display: flex;
  width: 33%;
  height: 40px;
  align-items: center;
}
</style>