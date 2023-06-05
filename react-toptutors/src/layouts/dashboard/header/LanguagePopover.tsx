import { useState } from 'react';
// @mui
import { MenuItem, Stack } from '@mui/material';
// locales
import { useLocales } from '../../../locales';
// components
import Image from '../../../components/image';
import MenuPopover from '../../../components/menu-popover';
import { IconButtonAnimate } from '../../../components/animate';

// ----------------------------------------------------------------------

export default function LanguagePopover() {
  const { currentLang, onChangeLang } = useLocales();

  const [openPopover, setOpenPopover] = useState<HTMLElement | null>(null);

  const handleOpenPopover = (event: React.MouseEvent<HTMLElement>) => {
    setOpenPopover(event.currentTarget);
  };

  const handleClosePopover = () => {
    setOpenPopover(null);
  };

  const handleChangeLang = (newLang: string) => {
    onChangeLang(newLang);
    handleClosePopover();
  };

  return (
    <>
      <IconButtonAnimate
        onClick={handleOpenPopover}
        sx={{
          width: 40,
          height: 40,
          ...(openPopover && {
            bgcolor: 'action.selected',
          }),
        }}
      >
        <Image disabledEffect src={currentLang.icon} alt={currentLang.label} />
      </IconButtonAnimate>

      <MenuPopover open={openPopover} onClose={handleClosePopover} sx={{ width: 180 }}>
        <Stack spacing={0.75}>
          {/* {allLangs.map((option) => (
            <MenuItem
              key={option.value}
              selected={option.value === currentLang.value}
              onClick={() => handleChangeLang(option.value)}
            >
              <Image
                disabledEffect
                alt={option.label}
                src={option.icon}
                sx={{ width: 28, mr: 2 }}
              />

              {option.label}
            </MenuItem>
          ))} */}
          <MenuItem key="da" selected onClick={() => handleChangeLang('da')}>
            <Image
              disabledEffect
              alt="Dansk"
              src="/assets/icons/flags/ic_flag_da.svg"
              sx={{ width: 28, mr: 2 }}
            />
            Dansk
          </MenuItem>
          <MenuItem key="en" disabled>
            <Image
              disabledEffect
              alt="English"
              src="/assets/icons/flags/ic_flag_en.svg"
              sx={{ width: 28, mr: 2 }}
            />
            English (Soon!)
          </MenuItem>
        </Stack>
      </MenuPopover>
    </>
  );
}
