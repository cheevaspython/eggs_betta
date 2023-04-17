<template>
  <form action="" style="width: 1000px">
    <div class="modal-card" style="width: 900px; height: 95vh">
      <header class="modal-card-head" style="background-color: #c3c3c3; text-align: center">
        <p class="modal-card-title" style="color: whitesmoke; font-size: 30px; font-weight: 900">Редактирование заявки от покупателя №{{applicationFromBuyer.id}}</p>
        <button
          type="button"
          class="delete"
          @click="$emit('close')"/>
      </header>

      <section class="modal-card-body is-fullwidth">
        <div class="card__title">Покупатель: {{ `${current_buyer.name} / ${current_buyer.inn}` }}</div>

        <div class="flexbox__row" style="width: 860px">
          <div class="flexbox__row flexbox__space-between input-border">
          <div style="width: calc(35% - 10px); margin-left: 10px">CB кол-во</div>
            <b-field class="my-b-input">
              <b-input placeholder="Введите количество" rounded v-model="cB"></b-input>
            </b-field>
          </div>
          <div class="flexbox__row flexbox__space-between input-border">
            <div style="margin-left: 10px">Стоимость за десяток</div>
            <b-field class="my-b-input-cost">
              <b-input placeholder="Введите сумму" rounded v-model="cB_cost"></b-input>
            </b-field>
          </div>
        </div>

        <div class="flexbox__row" style="width: 860px">
          <div class="flexbox__row flexbox__space-between input-border">
          <div style="width: calc(35% - 10px); margin-left: 10px">C0 кол-во</div>
            <b-field class="my-b-input">
              <b-input placeholder="Введите количество" rounded v-model="c0"></b-input>
            </b-field>
          </div>
          <div class="flexbox__row flexbox__space-between input-border">
            <div style="margin-left: 10px">Стоимость за десяток</div>
            <b-field class="my-b-input-cost">
              <b-input placeholder="Введите сумму" rounded v-model="c0_cost"></b-input>
            </b-field>
          </div>
        </div>

        <div class="flexbox__row" style="width: 860px">
          <div class="flexbox__row flexbox__space-between input-border">
          <div style="width: calc(35% - 10px); margin-left: 10px">C1 кол-во</div>
            <b-field class="my-b-input">
              <b-input placeholder="Введите количество" rounded v-model="c1"></b-input>
            </b-field>
          </div>
          <div class="flexbox__row flexbox__space-between input-border">
            <div style="margin-left: 10px">Стоимость за десяток</div>
            <b-field class="my-b-input-cost">
              <b-input placeholder="Введите сумму" rounded v-model="c1_cost"></b-input>
            </b-field>
          </div>
        </div>

        <div class="flexbox__row" style="width: 860px">
          <div class="flexbox__row flexbox__space-between input-border">
          <div style="width: calc(35% - 10px); margin-left: 10px">C2 кол-во</div>
            <b-field class="my-b-input">
              <b-input placeholder="Введите количество" rounded v-model="c2"></b-input>
            </b-field>
          </div>
          <div class="flexbox__row flexbox__space-between input-border">
            <div style="margin-left: 10px">Стоимость за десяток</div>
            <b-field class="my-b-input-cost">
              <b-input placeholder="Введите сумму" rounded v-model="c2_cost"></b-input>
            </b-field>
          </div>
        </div>

        <div class="flexbox__row" style="width: 860px">
          <div class="flexbox__row flexbox__space-between input-border">
          <div style="width: calc(35% - 10px); margin-left: 10px">C3 кол-во</div>
            <b-field class="my-b-input">
              <b-input placeholder="Введите количество" rounded v-model="c3"></b-input>
            </b-field>
          </div>
          <div class="flexbox__row flexbox__space-between input-border">
            <div style="margin-left: 10px">Стоимость за десяток</div>
            <b-field class="my-b-input-cost">
              <b-input placeholder="Введите сумму" rounded v-model="c3_cost"></b-input>
            </b-field>
          </div>
        </div>

        <div class="flexbox__row" style="width: 860px">
          <div class="flexbox__row flexbox__space-between input-border">
          <div style="width: calc(35% - 10px); margin-left: 10px">Грязь кол-во</div>
            <b-field class="my-b-input">
              <b-input placeholder="Введите количество" rounded v-model="dirt"></b-input>
            </b-field>
          </div>
          <div class="flexbox__row flexbox__space-between input-border">
            <div style="margin-left: 10px">Стоимость за десяток</div>
            <b-field class="my-b-input-cost">
              <b-input placeholder="Введите сумму" rounded v-model="dirt_cost"></b-input>
            </b-field>
          </div>
        </div>

        <div class="flexbox flexbox__row flexbox__space-between input-border" style="height: 450px; width: 100%;">
          <div class="flexbox__column" style=" padding: 10px 20px;">
            <div class="changeDates">Изменение окна поставки</div>
            <div class="flexbox__row flexbox__space-between" style="margin-top: 15px">
              <b-datepicker
                style="width: 360px;"
                inline
                range>
              </b-datepicker>
            </div>
          </div>
          <div class="flexbox__column" style="border-left: solid 2px #ebebeb;  padding: 10px 20px; height: 100%;">
            <div class="flexbox__column" style="margin: 0 auto; width: 250px;">
              <b-dropdown :triggers="['hover']" aria-role="list">
                <template #trigger>
                  <b-button
                    v-model="unloading_address"  
                    label="Изменение адреса разгрузки"
                    type="is-success is-light"
                    icon-right="menu-down" 
                    rounded />
                </template>
                  
                <b-dropdown-item v-if="warehouseAddress1" aria-role="listitem" @click="selectUnloadingAddress(warehouseAddress1)">
                  <strong>{{ warehouseAddress1 }}</strong></b-dropdown-item>
                <b-dropdown-item v-if="warehouseAddress2" aria-role="listitem" @click="selectUnloadingAddress(warehouseAddress2)">
                  <strong>{{ warehouseAddress2 }}</strong></b-dropdown-item>
                <b-dropdown-item v-if="warehouseAddress3" aria-role="listitem" @click="selectUnloadingAddress(warehouseAddress3)">
                  <strong>{{ warehouseAddress3 }}</strong></b-dropdown-item>
                <b-dropdown-item v-if="warehouseAddress4" aria-role="listitem" @click="selectUnloadingAddress(warehouseAddress4)">
                  <strong>{{ warehouseAddress4 }}</strong></b-dropdown-item>
                <b-dropdown-item v-if="warehouseAddress5" aria-role="listitem" @click="selectUnloadingAddress(warehouseAddress5)">
                  <strong>{{ warehouseAddress5 }}</strong></b-dropdown-item>
              </b-dropdown>
            </div>
            <div class="prod-address">
              {{ unloading_address }}
            </div>
            <div class="flexbox__row flexbox__space-between input-border" style="width: 100%;">
              <div style="margin-left: 10px">Отсрочка оплаты (дней):</div>
              <b-field class="my-b-input-cost" style="width: 40%;">
                <b-input placeholder="Введите кол-во дней" rounded v-model="postponementPay"></b-input>
              </b-field>
            </div>
          </div>
        </div>

        Комментарий:
        <b-field>
          <b-input v-model="comment" type="textarea" maxlength="255"></b-input>
        </b-field>
      </section>

      <footer class="modal-card-foot is-justify-content-flex-end">
        <b-button
          label="Подтвердить изменения"
          :loading="loading"
          type="is-success"
          @click="sendBuyerOrder"/>
        <b-button
          label="Закрыть"
          @click="$emit('close')"/>
      </footer>
    </div>
  </form>
</template>

<script>
export default {
  name: "ModalBuyerAppEditForm",
  props: ['applicationFromBuyer'],
  data() {
    return {
      loading: false,
      isPublic: true,
      updateDates: false,
      current_buyer: this.applicationFromBuyer.buyer_card_detail,
      cB: this.applicationFromBuyer.cB,
      cB_cost: this.applicationFromBuyer.cB_cost,
      c0: this.applicationFromBuyer.c0,
      c0_cost: this.applicationFromBuyer.c0_cost,
      c1: this.applicationFromBuyer.c1,
      c1_cost: this.applicationFromBuyer.c1_cost,
      c2: this.applicationFromBuyer.c2,
      c2_cost: this.applicationFromBuyer.c2_cost,
      c3: this.applicationFromBuyer.c3,
      c3_cost: this.applicationFromBuyer.c3_cost,
      dirt: this.applicationFromBuyer.dirt,
      dirt_cost: this.applicationFromBuyer.dirt_cost,
      warehouseAddress1: this.applicationFromBuyer.buyer_card_detail.warehouse_address_1,
      warehouseAddress2: this.applicationFromBuyer.buyer_card_detail.warehouse_address_2,
      warehouseAddress3: this.applicationFromBuyer.buyer_card_detail.warehouse_address_3,
      warehouseAddress4: this.applicationFromBuyer.buyer_card_detail.warehouse_address_4,
      warehouseAddress5: this.applicationFromBuyer.buyer_card_detail.warehouse_address_5,
      unloading_address: this.applicationFromBuyer.unloading_address,
      dates: [this.applicationFromBuyer.delivery_window_from, this.applicationFromBuyer.delivery_window_until],
      comment: this.applicationFromBuyer.comment,
      postponementPay: this.applicationFromBuyer.postponement_pay,
      newDates: [],
    }
  },
  methods: {
    getStrMonth(month) {
      switch (month) {
        case 0:
          return 'января'
        case 1:
          return 'февраля'
        case 2:
          return 'марта'
        case 3:
          return 'апреля'
        case 4:
          return 'мая'
        case 5:
          return 'июня'
        case 6:
          return 'июля'
        case 7:
          return 'августа'
        case 8:
          return 'сентября'
        case 9:
          return 'октября'
        case 10:
          return 'ноября'
        case 11:
          return 'декабря'
      }
    },
    getStrDay(dateStr) {
      const date = Date.parse(dateStr)
      const currentDate = new Date(date)
      return currentDate.getDate() + ' ' + this.getStrMonth(currentDate.getMonth()) + ' ' + currentDate.getFullYear()
    },
    removeRow() {
      this.selectedCategories.pop()
    },
    selectUnloadingAddress(address){
      this.unloading_address = address
    },
    checkDeliveryFrom(dates){
      if (this.updateDates.length > 0) {
        return dates[0].getDate() + '.' + (dates[0].getMonth() + 1) + '.' + dates[0].getFullYear()
      }
      else {
        return this.applicationFromBuyer.delivery_window_from
      }
    },
    checkDeliveryUntil(dates) {
      if (this.updateDates.length > 0) {
        return dates[1].getDate() + '.' + (dates[1].getMonth() + 1) + '.' + dates[1].getFullYear()
      }
      else {
        return this.applicationFromBuyer.delivery_window_until
      }
    },
    checkForComma(eggsCost) {
      let eggCost = `${eggsCost}`
      if (eggCost.includes(',')) {
        eggCost = eggCost.replace(',', '.')
      }
      return parseFloat(eggCost)
    },
    async sendBuyerOrder() {
      const data = {
        cB: this.cB,
        cB_cost: this.cB_cost ? this.checkForComma(this.cB_cost) : 0,
        c0: this.c0,
        c0_cost: this.c0_cost ? this.checkForComma(this.c0_cost) : 0,
        c1: this.c1,
        c1_cost: this.c1_cost ? this.checkForComma(this.c1_cost) : 0,
        c2: this.c2,
        c2_cost: this.c2_cost ? this.checkForComma(this.c2_cost) : 0,
        c3: this.c3,
        c3_cost: this.c3_cost ? this.checkForComma(this.c3_cost) : 0,
        dirt: this.dirt,
        dirt_cost: this.dirt_cost ? this.checkForComma(this.dirt_cost) : 0,
        unloading_address: this.unloading_address,
        delivery_window_from: this.checkDeliveryFrom(this.newDates),
        delivery_window_until: this.checkDeliveryUntil(this.newDates),
        postponement_pay: this.postponementPay,
        comment: this.comment
      }
      this.loading = true
      const id = this.applicationFromBuyer.id
      const success = await this.$store.dispatch('eggs/patchBuyerApp', [data, id])
        .finally(() => this.loading = false, setTimeout(this.update, 1000))
      if (!success) return
      const updatedBuyerApp = await this.$store.dispatch('eggs/getBuyerApp', id)
      await this.$store.dispatch('eggs/setCurrentAppFromBuyer', updatedBuyerApp)
      this.$emit('close')
    },
    update() {
      this.$store.dispatch('bid/getOwnerTasks')
      this.$store.dispatch('user/getUserNotifications')
    },
    clearFromDateTime() {
      this.dateFrom = null
    }
  },
}
</script>

<style lang="scss" scoped>
form {
  font-family: 'Montserrat';
}

.card {
  width: 100%;
  &__title {
    font-size: 22px;
    width: 100%;
    color: #5b5b5b;
    text-align: center;
    font-weight: 600;
    padding: 10px;
    border: 1px solid #dcdcdc;
    border-radius: 40px;
    margin-bottom: 15px;
    background-color: #e8ffe0;
  }
  &__row {
    display: flex;
    justify-content: space-between;
    margin-bottom: .5rem;
    border-bottom: solid #f5f5f5 2px;
  }
  &__row-end {
    display: flex;
    justify-content: space-between;
    margin-bottom: .5rem;
    border-bottom: solid #bfbfcf 4px;
  }
  &__info {
    overflow-wrap: break-word;
    max-width: 500px;
    font-weight: 500;
    margin-left: 1rem;
  }
  &__button-wrapper {
    margin-top: 20px;
    display: flex;
    justify-content: center;
  }
}

.input-border {
  border: solid 2px #ebebeb;
  border-radius: 20px;
  width: 50%;
  height: 40px;
  margin-bottom: 5px;
  align-items: center;
}

.my-b-input {
  width: 65%;
}

.my-b-input-cost {
  width: 50%;
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

.categories__calendar {
  display: grid;
  grid-template-columns: 1fr;
  gap: 40px;
  padding-bottom: 20px;
}

.changeDates {
  display: flex;
  color: white;
  justify-content: center;
  font-size: 18px;
  border-radius: 15px;
  background-color: #823bf570;
}

.prod-address {
  width: 100%;
  height: 26px;
  padding-bottom: 0px; 
  margin-top: 10px;
  margin-bottom: 10px; 
  text-align: center;
  background-color: #f5f5f5;
  border: solid 2px #ebebeb;
  border-top: 0;
  border-radius: 10px;
}
</style>
