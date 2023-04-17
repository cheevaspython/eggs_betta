<template>
  <form action="" style="width: 1000px">
    <div class="modal-card" style="width: 900px; height: 95vh">
      <header class="modal-card-head" style="background-color: #c3c3c3; text-align: center">
        <p class="modal-card-title" style="color: whitesmoke; font-size: 30px; font-weight: 900">Загрузка документов по Сделке №{{ deal.id }}</p>
        <button
          type="button"
          class="delete"
          @click="$emit('close')" />
      </header>

      <section class="modal-card-body is-fullwidth flexbox flexbox__column"> 
        <div class="upload-hint alert" style="margin-bottom: 10px; text-align: center;">Необходимый документ для продвижения статуса</div>

        <div class="flexbox__row flexbox__space-between input-border" style="width: 100%; padding-left: 15px; margin-bottom: 15px;">
          <div>Оплата по основному договору</div>
          <b-checkbox :value="true"
            type="is-success"
            size="is-medium"
            v-model="paymentForContract">
          </b-checkbox>
        </div>
    
        <div class="upload" v-bind:class="{ 'upload-hint': hintOnUpload('payment_order_incoming') }">
          <div>Платежное поручение входящее</div>
          <div v-show="toUpload.payment_order_incoming" class="rdy-to-download">Файл готов к загрузке</div>
          <div v-show="!toUpload.payment_order_incoming" class="hint">Нажмите чтобы загрузить</div>
          <input style="padding-bottom: 10px; z-index: 100;" accept=".pdf" type="file" 
            id="payment_order_incoming" ref="payment_order_incoming" @change="previewPayOrderIncoming" />
        </div>
        <div v-show="toUpload.payment_order_incoming" class="flexbox flexbox__row flexbox__space-between calendar-border">
          <div class="flexbox__column">
            <div class="changeDates">Дата документа</div>
              <div class="flexbox__row flexbox__space-between" style="margin-top: 15px">
              <b-datepicker
                style="width: 360px;"
                v-model="docDate"
                inline>
              </b-datepicker>
            </div>
          </div>
          <div class="flexbox__column" style="display: flex; padding-top: 50px;">
            <div class="flexbox__row flexbox__space-between input-border" style="width: 100%; margin-bottom: 5px">
              <div style="margin-left: 10px; margin-top: 8px">Номер документа</div>
              <b-field class="my-b-input">
                <b-input placeholder="Введите номер" v-model="docNumber" rounded></b-input>
              </b-field>
            </div>
            <div class="flexbox__row flexbox__space-between input-border" style="width: 100%; margin-bottom: 5px">
              <div style="margin-left: 10px; margin-top: 8px">Сумма ₽</div>
              <b-field class="my-b-input">
                <b-input placeholder="Введите сумму" v-model="docQuantity" rounded></b-input>
              </b-field>
            </div>
          </div>
        </div>

        <div class="upload" v-bind:class="{ 'upload-hint': hintOnUpload('payment_order_outcoming') }">
          <div>Платежное поручение исходящее</div>
          <div v-show="toUpload.payment_order_outcoming" class="rdy-to-download">Файл готов к загрузке</div>
          <div v-show="!toUpload.payment_order_outcoming" class="hint">Нажмите чтобы загрузить</div>
          <input style="padding-bottom: 10px; z-index: 100;" accept=".pdf" type="file" 
            id="payment_order_outcoming" ref="payment_order_outcoming" @change="previewPayOrderOutcoming" />
        </div>
        <div v-show="toUpload.payment_order_outcoming" class="flexbox flexbox__row flexbox__space-between calendar-border">
          <div class="flexbox__column">
            <div class="changeDates">Дата документа</div>
              <div class="flexbox__row flexbox__space-between" style="margin-top: 15px">
              <b-datepicker
                style="width: 360px;"
                v-model="docDate"
                inline>
              </b-datepicker>
            </div>
          </div>
          <div class="flexbox__column" style="display: flex; padding-top: 50px;">
            <div class="flexbox__row flexbox__space-between input-border" style="width: 100%; margin-bottom: 5px">
              <div style="margin-left: 10px; margin-top: 8px">Номер документа</div>
              <b-field class="my-b-input">
                <b-input placeholder="Введите номер" v-model="docNumber" rounded></b-input>
              </b-field>
            </div>
            <div class="flexbox__row flexbox__space-between input-border" style="width: 100%; margin-bottom: 5px">
              <div style="margin-left: 10px; margin-top: 8px">Сумма ₽</div>
              <b-field class="my-b-input">
                <b-input placeholder="Введите сумму" v-model="docQuantity" rounded></b-input>
              </b-field>
            </div>
          </div>
        </div>

        <div class="upload" v-bind:class="{ 'upload-hint': hintOnUpload('specification_seller') }">
          <div>Спецификация от продавца</div>
          <div v-show="toUpload.specification_seller" class="rdy-to-download">Файл готов к загрузке</div>
          <div v-show="!toUpload.specification_seller" class="hint">Нажмите чтобы загрузить</div>
          <input style="padding-bottom: 10px; z-index: 100;" accept=".pdf" type="file" 
            id="specification_seller" ref="specification_seller" @change="previewSpecSeller" />
        </div>
        <div class="upload" v-bind:class="{ 'upload-hint': hintOnUpload('account_to_seller') }">
          <div>Счет на оплату продавцу</div>
          <div v-show="toUpload.account_to_seller" class="rdy-to-download">Файл готов к загрузке</div>
          <div v-show="!toUpload.account_to_seller" class="hint">Нажмите чтобы загрузить</div>
          <input style="padding-bottom: 10px; z-index: 100;" accept=".pdf" type="file" 
            id="account_to_seller" ref="account_to_seller" @change="previewAccSeller" />
        </div>
        <div class="upload" v-bind:class="{ 'upload-hint': hintOnUpload('specification_buyer') }">
          <div>Спецификация от покупателя</div>
          <div v-show="toUpload.specification_buyer" class="rdy-to-download">Файл готов к загрузке</div>
          <div v-show="!toUpload.specification_buyer" class="hint">Нажмите чтобы загрузить</div>
          <input style="padding-bottom: 10px; z-index: 100;" accept=".pdf" type="file" 
            id="specification_buyer" ref="specification_buyer" @change="previewSpecBuyer" />
        </div>
        <div class="upload" v-bind:class="{ 'upload-hint': hintOnUpload('account_to_buyer') }">
          <div>Счет на оплату покупателю</div>
          <div v-show="toUpload.account_to_buyer" class="rdy-to-download">Файл готов к загрузке</div>
          <div v-show="!toUpload.account_to_buyer" class="hint">Нажмите чтобы загрузить</div>
          <input style="padding-bottom: 10px; z-index: 100;" accept=".pdf" type="file"
            id="account_to_buyer" ref="account_to_buyer" @change="previewAccBuyer" />
        </div>
        <div class="upload" v-bind:class="{ 'upload-hint': hintOnUpload('application_contract_logic') }">
          <div>Договор-заявка на транспорт</div>
          <div v-show="toUpload.application_contract_logic" class="rdy-to-download">Файл готов к загрузке</div>
          <div v-show="!toUpload.application_contract_logic" class="hint">Нажмите чтобы загрузить</div>
          <input style="padding-bottom: 10px; z-index: 100;" accept=".pdf" type="file" 
            id="application_contract_logic" ref="application_contract_logic" @change="previewContractLogic" />
        </div>
        <div class="upload" v-bind:class="{ 'upload-hint': hintOnUpload('account_to_logic') }">
          <div>Счет на транспорт</div>
          <div v-show="toUpload.account_to_logic" class="rdy-to-download">Файл готов к загрузке</div>
          <div v-show="!toUpload.account_to_logic" class="hint">Нажмите чтобы загрузить</div>
          <input style="padding-bottom: 10px; z-index: 100;" accept=".pdf" type="file" 
            id="account_to_logic" ref="account_to_logic" @change="previewAccLogic" />
        </div>
        <div class="upload" v-bind:class="{ 'upload-hint': hintOnUpload('UPD_incoming') }">
          <div>Входящая УПД</div>
          <div v-show="toUpload.UPD_incoming" class="rdy-to-download">Файл готов к загрузке</div>
          <div v-show="!toUpload.UPD_incoming" class="hint">Нажмите чтобы загрузить</div>
          <input style="padding-bottom: 10px; z-index: 100;" accept=".pdf" type="file" 
            id="UPD_incoming" ref="UPD_incoming" @change="previewUPDInc" />
        </div>
        <div v-show="toUpload.UPD_incoming" class="flexbox flexbox__row flexbox__space-between calendar-border">
          <div class="flexbox__column">
            <div class="changeDates">Дата документа</div>
              <div class="flexbox__row flexbox__space-between" style="margin-top: 15px">
              <b-datepicker
                style="width: 360px;"
                v-model="docDate"
                inline>
              </b-datepicker>
            </div>
          </div>
          <div class="flexbox__column" style="display: flex; padding-top: 50px;">
            <div class="flexbox__row flexbox__space-between input-border" style="width: 100%; margin-bottom: 5px">
              <div style="margin-left: 10px; margin-top: 8px">Номер документа</div>
              <b-field class="my-b-input">
                <b-input placeholder="Введите номер" v-model="docNumber" rounded></b-input>
              </b-field>
            </div>
            <div class="flexbox__row flexbox__space-between input-border" style="width: 100%; margin-bottom: 5px">
              <div style="margin-left: 10px; margin-top: 8px">Сумма ₽</div>
              <b-field class="my-b-input">
                <b-input placeholder="Введите сумму" v-model="docQuantity" rounded></b-input>
              </b-field>
            </div>
          </div>
        </div>

        <div class="upload" v-bind:class="{ 'upload-hint': hintOnUpload('account_invoicing_from_seller') }">
          <div>Счет-Фактура от продавца</div>
          <div v-show="toUpload.account_invoicing_from_seller" class="rdy-to-download">Файл готов к загрузке</div>
          <div v-show="!toUpload.account_invoicing_from_seller" class="hint">Нажмите чтобы загрузить</div>
          <input style="padding-bottom: 10px; z-index: 100;" accept=".pdf" type="file" 
            id="account_invoicing_from_seller" ref="account_invoicing_from_seller" @change="previewAccInvSeller" />
        </div>
        <div class="upload" v-bind:class="{ 'upload-hint': hintOnUpload('product_invoice_from_seller') }">
          <div>Товарная накладная от продавца</div>
          <div v-show="toUpload.product_invoice_from_seller" class="rdy-to-download">Файл готов к загрузке</div>
          <div v-show="!toUpload.product_invoice_from_seller" class="hint">Нажмите чтобы загрузить</div>
          <input style="padding-bottom: 10px; z-index: 100;" accept=".pdf" type="file" 
            id="product_invoice_from_seller" ref="product_invoice_from_seller" @change="previewProductInvSeller" />
        </div>
        <div class="upload" v-bind:class="{ 'upload-hint': hintOnUpload('UPD_outgoing') }">
          <div>Исходящая УПД</div>
          <div v-show="toUpload.UPD_outgoing" class="rdy-to-download">Файл готов к загрузке</div>
          <div v-show="!toUpload.UPD_outgoing" class="hint">Нажмите чтобы загрузить</div>
          <input style="padding-bottom: 10px; z-index: 100;" accept=".pdf" type="file" 
            id="UPD_outgoing" ref="UPD_outgoing" @change="previewUPDOut" />
        </div>
        <div v-show="toUpload.UPD_outgoing" class="flexbox flexbox__row flexbox__space-between calendar-border">
          <div class="flexbox__column">
            <div class="changeDates">Дата документа</div>
            <div class="flexbox__row flexbox__space-between" style="margin-top: 15px">
              <b-datepicker
                style="width: 360px;"
                v-model="docDate"
                inline>
              </b-datepicker>
            </div>
          </div>
          <div class="flexbox__column" style="display: flex; padding-top: 50px;">
            <div class="flexbox__row flexbox__space-between input-border" style="width: 100%; margin-bottom: 5px">
            <div style="margin-left: 10px; margin-top: 8px">Номер документа</div>
            <b-field class="my-b-input">
              <b-input placeholder="Введите номер" v-model="docNumber" rounded></b-input>
            </b-field>
          </div>
          <div class="flexbox__row flexbox__space-between input-border" style="width: 100%; margin-bottom: 5px">
            <div style="margin-left: 10px; margin-top: 8px">Сумма ₽</div>
              <b-field class="my-b-input">
                <b-input placeholder="Введите сумму" v-model="docQuantity" rounded></b-input>
              </b-field>
            </div>
          </div>
        </div>

        <div class="upload" v-bind:class="{ 'upload-hint': hintOnUpload('account_invoicing_from_buyer') }">
          <div>Счет-Фактура от покупателя</div>
          <div v-show="toUpload.account_invoicing_from_buyer" class="rdy-to-download">Файл готов к загрузке</div>
          <div v-show="!toUpload.account_invoicing_from_buyer" class="hint">Нажмите чтобы загрузить</div>
          <input style="padding-bottom: 10px; z-index: 100;" accept=".pdf" type="file" 
            id="account_invoicing_from_buyer" ref="account_invoicing_from_buyer" @change="previewAccInvBuyer" />
        </div>
        <div class="upload" v-bind:class="{ 'upload-hint': hintOnUpload('product_invoice_from_buyer') }">
          <div>Товарная накладная от покупателя</div>
          <div v-show="toUpload.product_invoice_from_buyer" class="rdy-to-download">Файл готов к загрузке</div>
          <div v-show="!toUpload.product_invoice_from_buyer" class="hint">Нажмите чтобы загрузить</div>
          <input style="padding-bottom: 10px; z-index: 100;" accept=".pdf" type="file" 
            id="product_invoice_from_buyer" ref="product_invoice_from_buyer" @change="previewProductInvBuyer" />
        </div>
        <div class="upload" v-bind:class="{ 'upload-hint': hintOnUpload('veterinary_certificate_buyer') }">
          <div>Ветеринарное свидетельсвто от покупателя</div>
          <div v-show="toUpload.veterinary_certificate_buyer" class="rdy-to-download">Файл готов к загрузке</div>
          <div v-show="!toUpload.veterinary_certificate_buyer" class="hint">Нажмите чтобы загрузить</div>
          <input style="padding-bottom: 10px; z-index: 100;" accept=".pdf" type="file" 
            id="veterinary_certificate_buyer" ref="veterinary_certificate_buyer" @change="previewVetCertBuyer" />
        </div>
        <div class="upload" v-bind:class="{ 'upload-hint': hintOnUpload('veterinary_certificate_seller') }">
          <div>Ветеринарное свидетельсвто от продавца</div>
          <div v-show="toUpload.veterinary_certificate_seller" class="rdy-to-download">Файл готов к загрузке</div>
          <div v-show="!toUpload.veterinary_certificate_seller" class="hint">Нажмите чтобы загрузить</div>
          <input style="padding-bottom: 10px; z-index: 100;" accept=".pdf" type="file" 
            id="veterinary_certificate_seller" ref="veterinary_certificate_seller" @change="previewVetCertSeller" />
        </div>
        <div class="upload" v-bind:class="{ 'upload-hint': hintOnUpload('international_deal_CMR') }">
          <div>Международная сделка, ЦМР</div>
          <div v-show="toUpload.international_deal_CMR" class="rdy-to-download">Файл готов к загрузке</div>
          <div v-show="!toUpload.international_deal_CMR" class="hint">Нажмите чтобы загрузить</div>
          <input style="padding-bottom: 10px; z-index: 100;" accept=".pdf" type="file" 
            id="international_deal_CMR" ref="international_deal_CMR" @change="previewCMR" />
        </div>
        <div class="upload" v-bind:class="{ 'upload-hint': hintOnUpload('international_deal_TTN') }">
          <div>Международная сделка, ТТН</div>
          <div v-show="toUpload.international_deal_TTN" class="rdy-to-download">Файл готов к загрузке</div>
          <div v-show="!toUpload.international_deal_TTN" class="hint">Нажмите чтобы загрузить</div>
          <input style="padding-bottom: 10px; z-index: 100;" accept=".pdf" type="file" 
            id="international_deal_TTN" ref="international_deal_TTN" @change="previewTTN" />
        </div>
        <div class="upload" v-bind:class="{ 'upload-hint': hintOnUpload('UPD_logic') }">
          <div>Транспортная УПД</div>
          <div v-show="toUpload.UPD_logic" class="rdy-to-download">Файл готов к загрузке</div>
          <div v-show="!toUpload.UPD_logic" class="hint">Нажмите чтобы загрузить</div>
          <input style="padding-bottom: 10px; z-index: 100;" accept=".pdf" type="file" 
            id="UPD_logic" ref="UPD_logic" @change="previewUPDLogic" />
        </div>
        <div class="upload" v-bind:class="{ 'upload-hint': hintOnUpload('account_invoicing_logic') }">
          <div>Транспортная счет-фактура</div>
          <div v-show="toUpload.account_invoicing_logic" class="rdy-to-download">Файл готов к загрузке</div>
          <div v-show="!toUpload.account_invoicing_logic" class="hint">Нажмите чтобы загрузить</div>
          <input style="padding-bottom: 10px; z-index: 100;" accept=".pdf" type="file" 
            id="account_invoicing_logic" ref="account_invoicing_logic" @change="previewAccInvLogic" />
        </div>
        <div class="upload" v-bind:class="{ 'upload-hint': hintOnUpload('product_invoice_logic') }">
          <div>Транспортная товарная накладная</div>
          <div v-show="toUpload.product_invoice_logic" class="rdy-to-download">Файл готов к загрузке</div>
          <div v-show="!toUpload.product_invoice_logic" class="hint">Нажмите чтобы загрузить</div>
          <input style="padding-bottom: 10px; z-index: 100;" accept=".pdf" type="file" 
            id="product_invoice_logic" ref="product_invoice_logic" @change="previewProductInvLogic" />
        </div>
      </section>

      <footer class="modal-card-foot is-justify-content-flex-end">
        <b-button
          label="Загрузить"
          :loading="loading"
          type="is-success"
          @click="loadDoc"/>
        <b-button
          label="Закрыть"
          @click="$emit('close')"/>
      </footer>
    </div>
  </form>
</template>

<script>
  export default {
    name: "ModalDealUploadForm",
    props: ['deal', 'docs'],
    data() {
      return {
        docsId: this.docs.id,
        loading: false,
        paymentForContract: this.docs.payment_for_contract,

        payment_order_incoming: this.docs.payment_order_incoming,
        payment_order_outcoming: this.docs.payment_order_outcoming,
        specification_seller: this.docs.specification_seller,
        account_to_seller: this.docs.account_to_seller,
        specification_buyer: this.docs.specification_buyer,
        account_to_buyer: this.docs.account_to_buyer,
        application_contract_logic: this.docs.application_contract_logic,
        account_to_logic: this.docs.account_to_logic,
        UPD_incoming: this.docs.UPD_incoming,
        account_invoicing_from_seller: this.docs.account_invoicing_from_seller,
        product_invoice_from_seller: this.docs.product_invoice_from_seller,
        UPD_outgoing: this.docs.UPD_outgoing,
        account_invoicing_from_buyer: this.docs.account_invoicing_from_buyer,
        product_invoice_from_buyer: this.docs.product_invoice_from_buyer,
        veterinary_certificate_buyer: this.docs.veterinary_certificate_buyer,
        veterinary_certificate_seller: this.docs.veterinary_certificate_seller,
        international_deal_CMR: this.docs.international_deal_CMR,
        international_deal_TTN: this.docs.international_deal_TTN,
        UPD_logic: this.docs.UPD_logic,
        account_invoicing_logic: this.docs.account_invoicing_logic,
        product_invoice_logic: this.docs.product_invoice_logic,
        toUpload: {
          payment_order_incoming: null,
          payment_order_outcoming: null,
          specification_seller: null,
          account_to_seller: null,
          specification_buyer: null,
          account_to_buyer: null,
          application_contract_logic: null,
          account_to_logic: null,
          UPD_incoming: null,
          account_invoicing_from_seller: null,
          product_invoice_from_seller: null,
          UPD_outgoing: null,
          account_invoicing_from_buyer: null,
          product_invoice_from_buyer: null,
          veterinary_certificate_buyer: null,
          veterinary_certificate_seller: null,
          international_deal_CMR: null,
          international_deal_TTN: null,
          UPD_logic: null,
          account_invoicing_logic: null,
          product_invoice_logic: null
        },

        docNumber: null,
        docDate: null,
        docQuantity: null
      }
    },
    created() {
      // console.log(this.deal)
    },
    methods: {
      hintOnUpload(doc) {
        switch (this.deal.deal_status) {
          case 2:
            if (doc == 'payment_order_outcoming') {
              return true
            }
            else {
              return false
            }
          case 4: 
            if (doc == 'account_to_seller') {
              return true
            }
            else {
              return false
            }
          case 5:
            if (doc == 'UPD_incoming') {
              return true
            }
            else {
              return false
            }
          case 7:
            if (doc == 'UPD_outgoing') {
              return true
            }
            else {
              return false
            }
          case 8:
            if (doc == 'UPD_outgoing') {
              return true
            }
            else {
              return false
            }
          default: 
            return false
        }
      },
      previewPayOrderIncoming() {
        if (this.toUpload.payment_order_outcoming || this.toUpload.UPD_incoming || this.toUpload.UPD_outgoing) {
          return alert('Нельзя одновременно загрузить:\n Платежное поручение входящее \n Платежное поручение исходящее  \n Входящая УПД \n Исходящая УПД')
        }
        this.toUpload.payment_order_incoming = this.$refs.payment_order_incoming.files[0]
      },
      previewPayOrderOutcoming() {
        if (this.toUpload.payment_order_incoming || this.toUpload.UPD_incoming || this.toUpload.UPD_outgoing) {
          return alert('Нельзя одновременно загрузить:\n Платежное поручение входящее \n Платежное поручение исходящее  \n Входящая УПД \n Исходящая УПД')
        }
        this.toUpload.payment_order_outcoming = this.$refs.payment_order_outcoming.files[0]
      },
      previewSpecSeller() {
        this.toUpload.specification_seller = this.$refs.specification_seller.files[0]
      },
      previewAccSeller() {
        this.toUpload.account_to_seller = this.$refs.account_to_seller.files[0]
      },
      previewSpecBuyer() {
        this.toUpload.specification_buyer = this.$refs.specification_buyer.files[0]
      },
      previewAccBuyer() {
        this.toUpload.account_to_buyer = this.$refs.account_to_buyer.files[0]
      },
      previewContractLogic() {
        this.toUpload.application_contract_logic = this.$refs.application_contract_logic.files[0]
      },
      previewAccLogic() {
        this.toUpload.account_to_logic = this.$refs.account_to_logic.files[0]
      },
      previewUPDInc() {
        if (this.toUpload.payment_order_outcoming || this.toUpload.payment_order_incoming || this.toUpload.UPD_outgoing) {
          return alert('Нельзя одновременно загрузить:\n Платежное поручение входящее \n Платежное поручение исходящее  \n Входящая УПД \n Исходящая УПД')
        }
        this.toUpload.UPD_incoming = this.$refs.UPD_incoming.files[0]
      },
      previewAccInvSeller() {
        this.toUpload.account_invoicing_from_seller = this.$refs.account_invoicing_from_seller.files[0]
      },
      previewProductInvSeller() {
        this.toUpload.product_invoice_from_seller = this.$refs.product_invoice_from_seller.files[0]
      },
      previewUPDOut() {
        if (this.toUpload.payment_order_outcoming || this.toUpload.payment_order_incoming || this.toUpload.UPD_incoming) {
          return alert('Нельзя одновременно загрузить:\n Платежное поручение входящее \n Платежное поручение исходящее  \n Входящая УПД \n Исходящая УПД')
        }
        this.toUpload.UPD_outgoing = this.$refs.UPD_outgoing.files[0]
      },
      previewAccInvBuyer() {
        this.toUpload.account_invoicing_from_buyer = this.$refs.account_invoicing_from_buyer.files[0]
      },
      previewProductInvBuyer() {
        this.toUpload.product_invoice_from_buyer = this.$refs.product_invoice_from_buyer.files[0]
      },
      previewVetCertBuyer() {
        this.toUpload.veterinary_certificate_buyer = this.$refs.veterinary_certificate_buyer.files[0]
      },
      previewVetCertSeller() {
        this.toUpload.veterinary_certificate_seller = this.$refs.veterinary_certificate_seller.files[0]
      },
      previewCMR() {
        this.toUpload.international_deal_CMR = this.$refs.international_deal_CMR.files[0]
      },
      previewTTN() {
        this.toUpload.international_deal_TTN = this.$refs.international_deal_TTN.files[0]
      },
      previewUPDLogic() {
        this.toUpload.UPD_logic = this.$refs.UPD_logic.files[0]
      },
      previewAccInvLogic() {
        this.toUpload.account_invoicing_logic = this.$refs.account_invoicing_logic.files[0]
      },
      previewProductInvLogic() {
        this.toUpload.product_invoice_logic = this.$refs.product_invoice_logic.files[0]
      },
      async loadDoc() {
        const formData = new FormData()
        if (this.paymentForContract != this.docs.payment_for_contract) {
          formData.append('payment_for_contract', this.paymentForContract)
        }
        if (this.toUpload.payment_order_incoming) {
          if (!this.docNumber) {
            return alert('Вы не ввели номер документа')
          }
          if (!this.docDate) {
            return alert('Вы не указали дату документа')
          }
          if (!this.docQuantity) {
            return alert('Вы не ввели сумму')
          }
          formData.append('payment_order_incoming', this.toUpload.payment_order_incoming)
          let day = `${this.docDate.getDate()}`
          day = (day.length == 1) ? '0' + day : day
          let month = `${this.docDate.getMonth() + 1}`
          month = (month.length == 1) ? '0' + month : month
          const date = day + '/' + month + '/' + this.docDate.getFullYear()
          const data_for_tmp_json = {
            date: date,
            number: this.docNumber,
            pay_quantity: this.docQuantity,
            inn: this.deal.buyer,
            doc_type: 'payment_order_incoming'
          }
          formData.append('tmp_json', JSON.stringify(data_for_tmp_json))
        }
        if (this.toUpload.payment_order_outcoming) {
          if (!this.docNumber) {
            return alert('Вы не ввели номер документа')
          }
          if (!this.docDate) {
            return alert('Вы не указали дату документа')
          }
          if (!this.docQuantity) {
            return alert('Вы не ввели сумму')
          }
          formData.append('payment_order_outcoming', this.toUpload.payment_order_outcoming)
          let day = `${this.docDate.getDate()}`
          day = (day.length == 1) ? '0' + day : day
          let month = `${this.docDate.getMonth() + 1}`
          month = (month.length == 1) ? '0' + month : month
          const date = day + '/' + month + '/' + this.docDate.getFullYear()
          const data_for_tmp_json = {
            date: date,
            number: this.docNumber,
            pay_quantity: this.docQuantity,
            inn: this.deal.seller,
            doc_type: 'payment_order_outcoming'
          }
          formData.append('tmp_json', JSON.stringify(data_for_tmp_json))
        }
        if (this.toUpload.specification_seller) {
          formData.append('specification_seller', this.toUpload.specification_seller)
          const data_for_tmp_json = {}
          formData.append('tmp_json', JSON.stringify(data_for_tmp_json))
        }
        if (this.toUpload.account_to_seller) {
          formData.append('account_to_seller', this.toUpload.account_to_seller)
          const data_for_tmp_json = {}
          formData.append('tmp_json', JSON.stringify(data_for_tmp_json))
        }
        if (this.toUpload.specification_buyer) {
          formData.append('specification_buyer', this.toUpload.specification_buyer)
          const data_for_tmp_json = {}
          formData.append('tmp_json', JSON.stringify(data_for_tmp_json))
        }
        if (this.toUpload.account_to_buyer) {
          formData.append('account_to_buyer', this.toUpload.account_to_buyer)
          const data_for_tmp_json = {}
          formData.append('tmp_json', JSON.stringify(data_for_tmp_json))
        }
        if (this.toUpload.application_contract_logic) {
          formData.append('application_contract_logic', this.toUpload.application_contract_logic)
          const data_for_tmp_json = {}
          formData.append('tmp_json', JSON.stringify(data_for_tmp_json))
        }
        if (this.toUpload.account_to_logic) {
          formData.append('account_to_logic', this.toUpload.account_to_logic)
          const data_for_tmp_json = {}
          formData.append('tmp_json', JSON.stringify(data_for_tmp_json))
        }
        if (this.toUpload.UPD_incoming) {
          if (!this.docNumber) {
            return alert('Вы не ввели номер документа')
          }
          if (!this.docDate) {
            return alert('Вы не указали дату документа')
          }
          if (!this.docQuantity) {
            return alert('Вы не ввели сумму')
          }
          formData.append('UPD_incoming', this.toUpload.UPD_incoming)
          let day = `${this.docDate.getDate()}`
          day = (day.length == 1) ? '0' + day : day
          let month = `${this.docDate.getMonth() + 1}`
          month = (month.length == 1) ? '0' + month : month
          const date = day + '/' + month + '/' + this.docDate.getFullYear()
          const data_for_tmp_json = {
            date: date,
            number: this.docNumber,
            pay_quantity: this.docQuantity,
            inn: this.deal.seller,
            doc_type: 'UPD_incoming'
          }
          formData.append('tmp_json', JSON.stringify(data_for_tmp_json))
        }
        if (this.toUpload.account_invoicing_from_seller) {
          formData.append('account_invoicing_from_seller', this.toUpload.account_invoicing_from_seller)
          const data_for_tmp_json = {}
          formData.append('tmp_json', JSON.stringify(data_for_tmp_json))
        }
        if (this.toUpload.product_invoice_from_seller) {
          formData.append('product_invoice_from_seller', this.toUpload.product_invoice_from_seller)
          const data_for_tmp_json = {}
          formData.append('tmp_json', JSON.stringify(data_for_tmp_json))
        }
        if (this.toUpload.UPD_outgoing) {
          if (!this.docNumber) {
            return alert('Вы не ввели номер документа')
          }
          if (!this.docDate) {
            return alert('Вы не указали дату документа')
          }
          if (!this.docQuantity) {
            return alert('Вы не ввели сумму')
          }
          formData.append('UPD_outgoing', this.toUpload.UPD_outgoing)
          let day = `${this.docDate.getDate()}`
          day = (day.length == 1) ? '0' + day : day
          let month = `${this.docDate.getMonth() + 1}`
          month = (month.length == 1) ? '0' + month : month
          const date = day + '/' + month + '/' + this.docDate.getFullYear()
          const data_for_tmp_json = {
            date: date,
            number: this.docNumber,
            pay_quantity: this.docQuantity,
            inn: this.deal.buyer,
            doc_type: 'UPD_outgoing'
          }
          formData.append('tmp_json', JSON.stringify(data_for_tmp_json))
        }
        if (this.toUpload.account_invoicing_from_buyer) {
          formData.append('account_invoicing_from_buyer', this.toUpload.account_invoicing_from_buyer)
          const data_for_tmp_json = {}
          formData.append('tmp_json', JSON.stringify(data_for_tmp_json))
        }
        if (this.toUpload.product_invoice_from_buyer) {
          formData.append('product_invoice_from_buyer', this.toUpload.product_invoice_from_buyer)
          const data_for_tmp_json = {}
          formData.append('tmp_json', JSON.stringify(data_for_tmp_json))
        }
        if (this.toUpload.veterinary_certificate_buyer) {
          formData.append('veterinary_certificate_buyer', this.toUpload.veterinary_certificate_buyer)
          const data_for_tmp_json = {}
          formData.append('tmp_json', JSON.stringify(data_for_tmp_json))
        }
        if (this.toUpload.veterinary_certificate_seller) {
          formData.append('veterinary_certificate_seller', this.toUpload.veterinary_certificate_seller)
          const data_for_tmp_json = {}
          formData.append('tmp_json', JSON.stringify(data_for_tmp_json))
        }
        if (this.toUpload.international_deal_CMR) {
          formData.append('international_deal_CMR', this.toUpload.international_deal_CMR)
          const data_for_tmp_json = {}
          formData.append('tmp_json', JSON.stringify(data_for_tmp_json))
        }
        if (this.toUpload.international_deal_TTN) {
          formData.append('international_deal_TTN', this.toUpload.international_deal_TTN)
          const data_for_tmp_json = {}
          formData.append('tmp_json', JSON.stringify(data_for_tmp_json))
        }
        if (this.toUpload.UPD_logic) {
          formData.append('UPD_logic', this.toUpload.UPD_logic)
          const data_for_tmp_json = {}
          formData.append('tmp_json', JSON.stringify(data_for_tmp_json))
        }
        if (this.toUpload.account_invoicing_logic) {
          formData.append('account_invoicing_logic', this.toUpload.account_invoicing_logic)
          const data_for_tmp_json = {}
          formData.append('tmp_json', JSON.stringify(data_for_tmp_json))
        }
        if (this.toUpload.product_invoice_logic) {
          formData.append('product_invoice_logic', this.toUpload.product_invoice_logic)
          const data_for_tmp_json = {}
          formData.append('tmp_json', JSON.stringify(data_for_tmp_json))
        }
        
        const docs = [this.docsId, formData]
        await this.$store.dispatch('eggs/dealUpload', docs)
        .finally( () => setTimeout(this.update, 1000))

        const updatedDeal =  await this.$store.dispatch('eggs/getModel', this.deal.id)
        await this.$store.dispatch('eggs/setCurrentDeal', updatedDeal)
        this.$emit('close')
      },
      update() {
        this.$store.dispatch('bid/getOwnerTasks')
        this.$store.dispatch('user/getUserNotifications')
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
    flex-flow: column;
  }
  &__row {
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
  &__button-wrapper {
    margin-top: 20px;
    display: flex;
    justify-content: center;
  }
  &__input {
    height: 1rem;
  }
}

.dropbox {
  outline: 2px dashed grey;
  outline-offset: -10px;
  background: lightcyan;
  color: dimgray;
  padding: 10px 10px;
  min-height: 200px;
  position: relative;
  cursor: pointer;
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

.alert {
  height: 30px;
  width: 100%;
  border-radius: 20px;
  margin-bottom: 15px;
  text-align: center;
}

.upload-hint {
  border: 3px solid orange;
}

.hint {
  color: orange;
  margin-left: 10px;
}

.rdy-to-download {
  margin-left: 10px;
  color: green;
}

.input-border {
  border: solid 2px #ebebeb;
  border-radius: 20px;
  width: 1060px;
  height: 44px;
  margin-bottom: 5px;
}

.my-b-input {
  width: 50%;
}

.calendar-border {
  border: solid 2px #ebebeb;
  border-radius: 20px;
  width: 100%;
  padding: 5px;
  margin-bottom: 5px;
}

.changeDates {
  display: flex;
  color: white;
  justify-content: center;
  font-size: 18px;
  border-radius: 15px;
  background-color: #823bf570;
}
</style>
