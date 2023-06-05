import { Page, View, Text, Image, Document } from '@react-pdf/renderer';
// utils
import { fDate } from '../../../../utils/formatTime';
import { fCurrency, fNumber } from '../../../../utils/formatNumber';
// @types
import { IPayslip } from '../../../../@types/payslip';
import { ITutor } from '../../../../@types/tutor';
//
import styles from './PayslipStyle';

// ----------------------------------------------------------------------

type Props = {
  payslip: IPayslip;
  tutor: ITutor;
};

export default function PayslipPDF({ payslip, tutor }: Props) {
  const { start_date, end_date, amount, referrals_amount, referrals_number, hours, id } = payslip;
  const { first_name, last_name, address, city } = tutor;
  return (
    <Document>
      <Page size="A4" style={styles.page}>
        <View style={[styles.gridContainer, styles.mb40]}>
          <Image source="/logo/logo_full.jpg" style={{ height: 32 }} />
          <View style={{ alignItems: 'flex-end', flexDirection: 'column' }}>
            <Text style={styles.h3}>Betalt</Text>
            <Text> {`Ref. nr.-${id}`} </Text>
          </View>
        </View>

        <View style={[styles.gridContainer, styles.mb40]}>
          <View style={styles.col6}>
            <Text style={[styles.overline, styles.mb8]}>Honorarseddel fra</Text>
            <Text style={styles.body1}>TopTutors ApS</Text>
            <Text style={styles.body1}>Porcelænshaven 26, 3</Text>
          </View>

          <View style={styles.col6}>
            <Text style={[styles.overline, styles.mb8]}>Invoice to</Text>
            <Text style={styles.body1}>
              {first_name} {last_name}
            </Text>
            <Text style={styles.body1}>
              {address}, {city}
            </Text>
          </View>
        </View>

        <View style={[styles.gridContainer, styles.mb40]}>
          <View style={styles.col6}>
            <Text style={[styles.overline, styles.mb8]}>Periode startdato</Text>
            <Text style={styles.body1}>{fDate(start_date)}</Text>
          </View>
          <View style={styles.col6}>
            <Text style={[styles.overline, styles.mb8]}>Periode slutdato</Text>
            <Text style={styles.body1}>{fDate(end_date)}</Text>
          </View>
        </View>

        <Text style={[styles.overline, styles.mb8]}>Honorarseddel detaljer</Text>

        <View style={styles.table}>
          <View style={styles.tableHeader}>
            <View style={styles.tableRow}>
              <View style={styles.tableCell_2}>
                <Text style={styles.subtitle2}>Beskrivelse</Text>
              </View>

              <View style={styles.tableCell_3}>
                <Text style={styles.subtitle2}>Antal timer</Text>
              </View>

              <View style={styles.tableCell_3}>
                <Text style={styles.subtitle2}>Timeløn</Text>
              </View>
              <View style={styles.tableCell_3}>
                <Text style={styles.subtitle2}>Referrals amount</Text>
              </View>
              <View style={styles.tableCell_3}>
                <Text style={styles.subtitle2}>Referrals number</Text>
              </View>

              <View style={[styles.tableCell_3, styles.alignRight]}>
                <Text style={styles.subtitle2}>I alt</Text>
              </View>
            </View>
          </View>

          <View style={styles.tableBody}>
            <View style={styles.tableRow}>
              <View style={styles.tableCell_2}>
                <Text style={styles.subtitle2}>Undervisningstimer</Text>
                <Text>description</Text>
              </View>

              <View style={styles.tableCell_3}>
                <Text>{hours}</Text>
              </View>

              <View style={styles.tableCell_3}>
                <Text>{fCurrency((amount - referrals_amount) / hours)}</Text>
              </View>
              <View style={styles.tableCell_3}>
                <Text>{fCurrency(referrals_amount)}</Text>
              </View>
              <View style={styles.tableCell_3}>
                <Text>{fNumber(referrals_number)}</Text>
              </View>
              <View style={[styles.tableCell_3, styles.alignRight]}>
                <Text>{fCurrency(amount)}</Text>
              </View>
            </View>

            {/* <View style={styles.tableRow}>
              <View style={styles.tableCell_2}>
                <Text style={styles.subtitle2}>Henvisninger</Text>
                <Text>Description</Text>
              </View>

              <View style={styles.tableCell_3}>
                <Text>quantity</Text>
              </View>

              <View style={styles.tableCell_3}>
                <Text>item.price</Text>
              </View>

              <View style={[styles.tableCell_3, styles.alignRight]}>
                <Text>fCurrency(item.price * item.quantity)</Text>
              </View>
            </View> */}

            <View style={[styles.tableRow, styles.noBorder]}>
              <View style={styles.tableCell_1} />
              <View style={styles.tableCell_2} />
              <View style={styles.tableCell_3} />
              <View style={styles.tableCell_3}>
                <Text style={styles.h4}>Total</Text>
              </View>
              <View style={[styles.tableCell_3, styles.alignRight]}>
                <Text style={styles.h4}>{fCurrency(amount)}</Text>
              </View>
            </View>
          </View>
        </View>

        {/* <View style={[styles.gridContainer, styles.footer]}>
          <View style={styles.col8}>
            <Text style={styles.subtitle2}>NOTES</Text>
            <Text>
              We appreciate your business. Should you need us to add VAT or extra notes let us know!
            </Text>
          </View>
          <View style={[styles.col4, styles.alignRight]}>
            <Text style={styles.subtitle2}>Have a Question?</Text>
            <Text>support@abcapp.com</Text>
          </View>
        </View> */}
      </Page>
    </Document>
  );
}
