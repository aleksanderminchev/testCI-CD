/* follow this path to see where the inspiration for this code comes from in the Minimal_TypeScript_v4.2.0:

src/sections/@dashboard/user/list/UserTableToolbar
*/

import { Stack, Button } from '@mui/material';
// components
import Iconify from '../../../components/iconify';

type Props = {
  onResetFilter: VoidFunction;
  isFiltered: boolean;
};

export default function ResetButton({ onResetFilter, isFiltered }: Props) {
  return (
    <Stack
      spacing={2}
      alignItems="center"
      direction={{
        xs: 'column',
        sm: 'row',
      }}
      sx={{ px: 2.5, py: 3 }}
    >
      {isFiltered && (
        <Button
          color="error"
          sx={{ flexShrink: 0 }}
          onClick={onResetFilter}
          startIcon={<Iconify icon="eva:trash-2-outline" />}
        >
          Clear
        </Button>
      )}
    </Stack>
  );
}
