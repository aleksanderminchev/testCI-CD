/* follow this path to get to where the code is inspired from in the Minimal_TypeScript_v4.2.0:

src/sections/@dashboard/file/filter/FileFilterButton
*/

// @mui
import { Box, Button, ButtonProps } from '@mui/material';

// ----------------------------------------------------------------------

interface Props extends ButtonProps {
  children?: React.ReactNode;
  isSelected: boolean;
}

export default function FileFilterButton({ children, isSelected, ...other }: Props) {
  return (
    <Button
      variant="soft"
      color="inherit"
      sx={{
        textTransform: 'unset',
        color: 'text.secondary',
        width: { xs: 1, md: 'auto' },
        justifyContent: 'flex-start',
        fontWeight: 'fontWeightMedium',
        ...(isSelected && {
          color: 'text.primary',
        }),
      }}
      {...other}
    >
      {children}

      <Box sx={{ flexGrow: 1 }} />
    </Button>
  );
}
