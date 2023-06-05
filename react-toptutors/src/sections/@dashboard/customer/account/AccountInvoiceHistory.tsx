// @mui
import { Stack, Link, Typography } from '@mui/material';

import { useState } from 'react';

// utils
import { fDate } from '../../../../utils/formatTime';
import { fCurrency } from '../../../../utils/formatNumber';
// @types
import { IUserAccountBillingInvoice } from '../../../../@types/user';
// components

import NavigateButton from '../../components/NavigateButton';
// ----------------------------------------------------------------------

type Props = {
  invoices: IUserAccountBillingInvoice[];
  customer_id: string;
};

export default function AccountBillingInvoiceHistory({ invoices, customer_id }: Props) {
  const [openInvoiceList, setOpenInvoiceList] = useState(false);

  const handleOpenInvoiceList = () => {
    setOpenInvoiceList(true);
  };

  return (
    <Stack spacing={3} alignItems="flex-end">
      <Typography variant="overline" sx={{ width: 1, color: 'text.secondary' }}>
        Invoice History
      </Typography>

      <Stack spacing={2} sx={{ width: 1 }}>
        {invoices.map((invoice) => (
          <Stack key={invoice.id} direction="row" justifyContent="space-between" sx={{ width: 1 }}>
            <Typography variant="body2" sx={{ minWidth: 120 }}>
              {fDate(invoice.createdAt)}
            </Typography>

            <Typography variant="body2">{fCurrency(invoice.price)}</Typography>

            <Link>PDF</Link>
          </Stack>
        ))}
      </Stack>

      <NavigateButton
        link={`invoice/${customer_id}`}
        onOpen={handleOpenInvoiceList}
        sx={{ mb: 5 }}
      />
    </Stack>
  );
}
